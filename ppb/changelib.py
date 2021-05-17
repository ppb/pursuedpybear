"""
Helpers for declaring deprecations, changes, renames, etc.
"""
import functools
import typing

from deprecated.sphinx import deprecated, versionadded, versionchanged

__all__ = [
    'deprecated', 'versionadded', 'versionchanged',
    'renamed',
]


def renamed(old: str, new: typing.Any, *, version: str, **kwargs):
    """
    Creates a name alias for a function, class, or method.

    :param str reason:
        Reason message which documents the rename.

    :param str version:
        Version in which this rename occurred.
    """

    if isinstance(new, type):
        # A class
        kwargs.setdefault("reason", f"Use {new.__name__} instead")
        wrapper = type(old, (new,), {})
        return deprecated(version=version, **kwargs)(wrapper)
    elif callable(new):
        # A function
        kwargs.setdefault("reason", f"Use {new.__name__} instead")

        @functools.wraps(new)
        def wrapper(*p, **kw):
            return new(*p, **kw)
        wrapper.__name__ = old
        return deprecated(version=version, **kwargs)(wrapper)
    else:
        # Dunno how to warn on usage for this.
        return new
