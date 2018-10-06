"""
ppb.flags contains singletons to communicate various things.

Use like None:
    * compare against using `is`
    * Don't instantiate a new instance.
"""

__all__ = 'Flag', 'DoNotRender'


class FlagMeta(type):
    _instance = None
    def __new__(mcls, *p, abstract=False, **kw):
        cls = super().__new__(mcls, *p, **kw)
        print("__new__", mcls, cls, p, kw)
        if abstract:
            return cls
        else:
            return cls()

    def __call__(cls, *p, **kw):
        if cls._instance is None:
            cls._instance = super().__call__(*p, **kw)
        return cls._instance


class Flag(metaclass=FlagMeta, abstract=True):
    """Inherit from Flag to make a simple class flag."""
    def __new__(cls, *args, **kwargs):
        return cls


class DoNotRender(Flag):
    """Inform the renderer to ignore this object."""


