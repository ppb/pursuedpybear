import logging
import sys
import numbers
import math

__all__ = 'LoggingMixin', 'FauxFloat',


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


class FauxFloat(numbers.Real):
    """
    When applied to a class that implements __float__, provides the full suite
    of number-related special methods.

    While this mixin doesn't do anything about it, you should consider making
    your class immutable. Odd things could potentially happen otherwise.
    """

    def __abs__(self):
        return abs(float(self))

    def __add__(self, other):
        return float(self) + other

    def __ceil__(self):
        return math.ceil(float(self))

    def __eq__(self, other):
        return float(self) == other

    def __floor__(self):
        return math.floor(float(self))

    def __floordiv__(self, other):
        return float(self) // other

    def __ge__(self, other):
        return float(self) >= other

    def __gt__(self, other):
        return float(self) > other

    def __le__(self, other):
        return float(self) <= other

    def __lt__(self, other):
        return float(self) < other

    def __mod__(self, other):
        return float(self) % other

    def __mul__(self, other):
        return float(self) * other

    def __neg__(self):
        return -float(self)

    def __pos__(self):
        return +float(self)

    def __pow__(self, other):
        return float(self) ** other

    def __radd__(self, other):
        return other + float(self)

    def __rfloordiv__(self, other):
        return other // float(self)

    def __rmod__(self, other):
        return other % float(self)

    def __rmul__(self, other):
        return other * float(self)

    def __round__(self, ndigits=None):
        return round(float(self), ndigits)

    def __rpow__(self, other):
        return other ** float(self)

    def __rtruediv__(self, other):
        return other / float(self)

    def __truediv__(self, other):
        return float(self) / other

    def __trunc__(self):
        return math.trunc(float(self))
