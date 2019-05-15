"""
Field declaration system.

This allows applying coercion and other code to both instances and subclasses.

class Spam(FieldMixin):
    class Fields:
        eggs: str
        foo = BarProperty()

Basically, what this does is let you keep property descriptors off the class and
apply them to class values.
"""
import inspect


__all__ = 'FieldMixin', 'iterfields', 'typefield', 'conversionfield',  'virtualfield'


def _annotations_to_fields(annos):
    """
    Converts an annotations dict into a fields dict
    """
    return {
        name: typefield(anno)
        for name, anno in annos.items()
        if isinstance(anno, type)  # Skip complex annotations
    }


def _iter_nonspecial_props(obj):
    for name, value in vars(obj).items():
        if not name.startswith('_'):
            yield name, value


def _build_fields_dict(cls, fieldbag):
    if hasattr(fieldbag, '__annotations__'):
        # In this order so that assigned values override annotations
        rv = _annotations_to_fields(fieldbag.__annotations__)
        rv.update(_iter_nonspecial_props(fieldbag))
    else:
        rv = dict(_iter_nonspecial_props(fieldbag))

    # Re-call __set_name__ to correct the owner
    for name, field in rv.items():
        field.__set_name__(cls, name)

    return rv


def _build_annotations(cls, fieldbag):
    if hasattr(cls, '__annotations__'):
        rv = cls.__annotations__
    else:
        rv = {}
    if hasattr(fieldbag, '__annotations__'):
        rv.update(fieldbag.__annotations__)

    for name, field in vars(fieldbag).items():
        # Explicit annotations override annotations inferred from fields
        # This is reverse of the fields themselves
        if hasattr(field, '__annotation__') and name not in rv:
            rv[name] = field.__annotation__
    return rv


class FieldMixin:
    """
    Mixin that implements all the field magic
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # If new fields are defined, make a __fields__
        if hasattr(cls, 'Fields') and isinstance(cls.Fields, type):
            fieldbag = cls.Fields
            del cls.Fields

            cls.__fields__ = _build_fields_dict(cls, fieldbag)
            cls.__annotations__ = _build_annotations(cls, fieldbag)

        # Run any fields on values defined on the class level
        varsdict = vars(cls)
        for name, field in iterfields(cls):
            if name in varsdict:
                # This is kind of an abuse of the interface and I hope it
                # doesn't blow up in an obscure way.
                field.__set_class__(cls, varsdict[name])

    def __init__(self, **fields):
        super().__init__()
        for name, value in fields.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        for cls in type(self).mro():
            if hasattr(cls, '__fields__'):
                if name in cls.__fields__:
                    cls.__fields__[name].__set__(self, value)
                    return
        else:
            super().__setattr__(name, value)

    def __getattribute__(self, name):
        for cls in type(self).mro():
            if hasattr(cls, '__fields__'):
                if name in cls.__fields__:
                    return cls.__fields__[name].__get__(self, cls)
        else:
            return super().__getattribute__(name)

    def __delattr__(self, name):
        for cls in type(self).mro():
            if hasattr(cls, '__fields__'):
                if name in cls.__fields__:
                    cls.__fields__[name].__delete__(self)
                    return
        else:
            super().__delattr__(name)


def iterfields(object):
    """
    Generates pairs of (name:str, field:object)
    """
    if not isinstance(object, type):
        object = type(object)

    seen_names = set()
    for cls in object.mro():
        if hasattr(cls, '__fields__'):
            for name, field in cls.__fields__.items():
                if name not in seen_names:
                    yield name, field
                    seen_names.add(name)


class typefield:
    """
    A field that coerces to the given type, if it's not already the type.

        spam = typefield(Foo)
    """
    def __init__(self, type):
        self.type = type
        self.__annotation__ = type

    def __get__(self, instance, owner):
        try:
            return instance.__dict__[self.key]
        except KeyError:
            raise AttributeError

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            value = self.type(value)

        instance.__dict__[self.key] = value

    def __set_class__(self, cls, value):
        if not isinstance(value, self.type):
            value = self.type(value)

        setattr(cls, self.key, value)
        # We don't use setattr() in most places to avoid weird recursion problems

    def __delete__(self, instance):
        del instance.__dict__[self.key]

    def __set_name__(self, owner, name):
        self.key = name


class conversionfield:
    """
    @conversionfield
    def spam(value):
        return float(value) % 360

    spam = conversion field(lambda value: float(value) % 360)

    A field that runs the given converter on set
    """
    def __init__(self, converter):
        self.converter = converter
        sig = inspect.signature(converter)
        if sig.return_value is not inspect.Signature.empty:
            self.__annotation__ = sig.return_value

    def __get__(self, instance, owner):
        try:
            return instance.__dict__[self.key]
        except KeyError:
            raise AttributeError

    def __set__(self, instance, value):
        instance.__dict__[self.key] = self.converter(value)

    def __set_class__(self, cls, value):
        setattr(cls, self.key, self.converter(value))

    def __delete__(self, instance):
        del instance.__dict__[self.key]

    def __set_name__(self, owner, name):
        self.key = name


class virtualfield(property):
    """
    A fully synthetic field.

    Use exactly like property.
    """

    @property
    def __annotation__(self):
        if getattr(self, 'fget', None):
            sig = inspect.signature(self.fget)
            if sig.return_value is not inspect.Signature.empty:
                return sig.return_value

    def __set_class__(self, cls, value):
        pass
