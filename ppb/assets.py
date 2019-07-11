"""
The asset loading system.
"""

import concurrent.futures
import threading

import ppb.vfs as vfs


_executor = concurrent.futures.ThreadPoolExecutor()
_resources = {}  # maps resource names to futures


class Asset:
    """
    A resource to be loaded from the filesystem and used.

    Meant to be subclassed.
    """
    def __init__(self, name):
        self.name = name
        self._finished = threading.Event()
        hint(name, self._finished_background)

    def _finished_background(self, fut):
        # Internal
        # Called in background thread
        try:
            raw = fut.result()
        except Exception:
            # Don't do anything here, forward it to the main thread instead
            pass
        else:
            self._data = self.background_parse(raw)

    def background_parse(self, data):
        """
        Takes the bytes from the resource and returns the parsed data.

        Subclasses probably want to override this.

        Called in the background thread.
        """
        return data

    def is_loaded(self):
        """
        Returns if the data has been loaded and parsed.
        """
        return self._finished.is_set()

    def load(self, timeout=None):
        """
        Gets the parsed data.

        Will block if not finished.
        """
        self._finished.wait(timeout)
        return self._data


def _load(filename):
    with vfs.open(filename) as file:
        return file.read()


def hint(filename, callback=None):
    """
    Hint that a resource will probably be needed
    """
    _resources[filename] = _executor.submit(_load, filename)
    if callback is not None:
        _resources[filename].add_done_callback(callback)


def load(filename):
    """
    Get the contents of a resource
    """
    if filename not in _resources:
        hint(filename)
    return _resources[filename].result()
