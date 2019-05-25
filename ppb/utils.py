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
        return float(self).__abs__()

    def __add__(self, other):
        return float(self).__add__(other)

    def __ceil__(self):
        return math.ceil(float(self))

    def __eq__(self, other):
        return float(self).__eq__(other)

    def __float__(self, other):
        return float(self).__float__(other)

    def __floor__(self):
        return math.floor(float(self))

    def __floordiv__(self, other):
        return float(self).__floordiv__(other)

    def __ge__(self, other):
        return float(self).__ge__(other)

    def __gt__(self, other):
        return float(self).__gt__(other)

    def __le__(self, other):
        return float(self).__le__(other)

    def __lt__(self, other):
        return float(self).__lt__(other)

    def __mod__(self, other):
        return float(self).__mod__(other)

    def __mul__(self, other):
        return float(self).__mul__(other)

    def __neg__(self):
        return float(self).__neg__()

    def __pos__(self):
        return float(self).__pos__()

    def __pow__(self, other):
        return float(self).__pow__(other)

    def __radd__(self, other):
        return float(self).__radd__(other)

    def __rfloordiv__(self, other):
        return float(self).__rfloordiv__(other)

    def __rmod__(self, other):
        return float(self).__rmod__(other)

    def __rmul__(self, other):
        return float(self).__rmul__(other)

    def __round__(self, ndigits=None):
        return float(self).__round__(ndigits)

    def __rpow__(self, other):
        return float(self).__rpow__(other)

    def __rtruediv__(self, other):
        return float(self).__rtruediv__(other)

    def __truediv__(self, other):
        return float(self).__truediv__(other)

    def __trunc__(self):
        return float(self).__trunc__()
