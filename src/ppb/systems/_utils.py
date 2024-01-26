import collections.abc
import functools
import weakref

__all__ = 'ObjectSideData',


def _drop(self_ref, key, ref):
    self = self_ref()
    if self is not None:
        try:
            del self._data[key]
        except KeyError:
            pass


class ObjectSideData(collections.abc.MutableMapping):
    """
    Similar to a WeakKeyDictionary, but tracks against object identity instead
    of object value.
    """
    def __init__(self, values=None):
        self._data = {}  # id: (ref, value)
        if values:
            self.update(values)

    def __getitem__(self, key):
        _, value = self._data[id(key)]
        return value

    def __delitem__(self, key):
        del self._data[id(key)]

    def __iter__(self):
        for ref, _ in self._data.values():
            key = ref()
            if key is not None:
                yield key

    def __len__(self):
        return len(self._data)

    def __setitem__(self, key, value):
        ref = weakref.ref(
            key,
            functools.partial(_drop, weakref.ref(self), id(key))
        )
        self._data[id(key)] = (ref, value)
