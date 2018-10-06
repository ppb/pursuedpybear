"""
ppb.flags contains singletons to communicate various things.

Use like None:
    * compare against using `is`
    * Don't instantiate a new instance.
"""

__all__ = 'Flag', 'DoNotRender'


class FlagMeta(type):
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
    """Inherit from Flag to make a simple class flag."""


class DoNotRender(Flag):
    """Inform the renderer to ignore this object."""
