"""
ppb.flags contains singletons to communicate various things.

Flags should be used like None and ... (Ellipsis):
* compare against using `is`
* Do not instantiate new instances

New flags can simply be defined by:

    class MyFlag(Flag):
        "This is a flag to indicate a thing."


New classes of flags (eg mouse buttons) can be defined as:

    class MyFlagType(Flag, abstract=True):
        "A group of indicators"

    class MyFlag(MyFlagType):
        "This is a flag to indicate a thing."
"""

__all__ = 'Flag',


class FlagMeta(type):
    """
    Metaclass for Flag. You probably want that instead.
    """
    def __new__(mcls, *p, abstract=False, **kw):
        cls = super().__new__(mcls, *p, **kw)
        if abstract:
            cls._instance = ...
            return cls
        else:
            cls._instance = None
            return cls()

    def __call__(cls):
        if cls._instance is None:
            cls._instance = type.__call__(cls)
        elif cls._instance is ...:
            raise TypeError("Cannot instantiate abstract flags")
        return cls._instance


class Flag(metaclass=FlagMeta, abstract=True):
    """
    Inherit from Flag to make a simple flag.

    Add abstract=True in the class line to make a flag type.
    """


class BlendMode(Flag, abstract=True):
    """
    A flag indicating a blend mode, changing how translucent sprites are drawn
    over top of other sprites.
    """


class BlendModeAdd(BlendMode):
    """
    Indicate a sprite, if translucent, should be rendered in ADD mode.
    """


class BlendModeBlend(BlendMode):
    """
    Indicate a sprite, if translucent, should be rendered in BLEND mode.
    """


class BlendModeMod(BlendMode):
    """
    Indicate a sprite, if translucent, should be rendered in MOD mode.
    """


class BlendModeNone(BlendMode):
    """
    Indicate a sprite, if translucent, should be rendered in NONE mode.
    """
