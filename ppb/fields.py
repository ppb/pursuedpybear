"""
Field declaration system.

This allows applying coercion and other code to both instances and subclasses.

class Spam(FieldMixin):
    class Fields:
        eggs: str
        foo = BarProperty()
"""

__all__ = 'FieldMixin', 'iterfields',  # 'field', 'virtualfield'


def _annotations_to_fields(annos):
    """
    Converts an annotations dict into a fields dict
    """


class FieldMixin:
    """
    Mixin that implements all the field magic
    """
    def __init_subclass__(cls, **_):
        # If new fields are defined, make a __fields__
        if hasattr(cls, 'Fields') and isinstance(cls.Fields, type):
            fieldbag = cls.Fields
            del cls.Fields

            if hasattr(cls, '__annotations__'):
                # In this order so that assigned values override annotations
                cls.__fields__ = _annotations_to_fields(cls.__annotations__)
                cls.__fields__.update(vars(fieldbag))
            else:
                cls.__fields__ = vars(fieldbag)

            # TODO: Update the __annotations__ of cls

        # Run any fields on values defined on the class level
        varsdict = vars(cls)
        for name, _ in iterfields(cls):
            if name in varsdict:
                # TODO: Actually run the set
                varsdict[name] = ...(varsdict[name])

    def __setattr__(self, name, value):
        for cls in type(self).mro():
            if hasattr(cls, '__fields__'):
                if name in cls.__fields__:
                    # TODO: Actually run the set
                    ...
                    break
        else:
            super().__setattr__(name, value)

    def __getattribute__(self, name):
        for cls in type(self).mro():
            if hasattr(cls, '__fields__'):
                if name in cls.__fields__:
                    # TODO: Actually run the get
                    ...
                    break
        else:
            super().__getattribute__(name)

    def __delattr__(self, name):
        for cls in type(self).mro():
            if hasattr(cls, '__fields__'):
                if name in cls.__fields__:
                    # TODO: Actually run the del
                    ...
                    break
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
