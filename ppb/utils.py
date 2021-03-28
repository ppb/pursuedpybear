import logging
import re
import sys
from time import perf_counter
import typing

__all__ = 'LoggingMixin', 'camel_to_snake', 'get_time', 'Color'


Color = typing.Tuple[int, int, int]

# Dictionary mapping file names -> module names
_module_file_index = {}


def _build_index():
    """
    Rebuild _module_file_index from sys.modules
    """
    global _module_file_index
    _module_file_index = {
        mod.__file__: mod.__name__
        for mod in sys.modules.values()
        if hasattr(mod, '__file__') and hasattr(mod, '__name__')
    }


_boundaries_finder = re.compile('(.)([A-Z][a-z]+)')
_boundaries_finder_2 = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(txt):
    s1 = _boundaries_finder.sub(r'\1_\2', txt)
    return _boundaries_finder_2.sub(r'\1_\2', s1).lower()


def get_time():
    """
    Returns the time via the default timer.
    
    Currently uses :func:`time.perf_counter` as the default timer.
    
    .. warning:: This is not a globally synchronized timer, it's just simply a system time. It is intended
       to make sure all timers in ppb code use the same function.
    """
    return perf_counter()


def _get_module(file_name):
    """
    Find the module name for the given file name, or raise KeyError if it's
    not a loaded module.
    """
    if file_name not in _module_file_index:
        _build_index()
    return _module_file_index[file_name]


class LoggingMixin:
    """
    A simple mixin to provide a `logger` attribute to instances, based on their
    module.
    """

    @property
    def logger(self):
        """
        The logger for this class.
        """
        # This is internal/CPython only/etc
        # It's also astonishingly faster than alternatives.
        frame = sys._getframe(1)
        file_name = frame.f_code.co_filename

        module_name = _get_module(file_name)
        return logging.getLogger(module_name)
