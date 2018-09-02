"""
ppb.flags contains singletons to communicate various things.

Use like None:
    * compare against using `is`
    * Don't instantiate a new instance.
"""


class Flag:
    """Inherit from Flag to make a simple class flag."""
    def __new__(cls, *args, **kwargs):
        return cls


class DoNotRender(Flag):
    """Inform the renderer to ignore this object."""


