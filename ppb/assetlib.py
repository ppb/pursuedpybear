"""
The asset loading system.
"""
import abc
import collections
import concurrent.futures
from functools import partial
import logging
import queue
import sys
import threading
import weakref

import ppb.vfs as vfs
import ppb.events as events
from ppb.systemslib import System

__all__ = 'AbstractAsset', 'Asset', 'AssetLoadingSystem',

logger = logging.getLogger(__name__)


class DelayedThreadExecutor(concurrent.futures.ThreadPoolExecutor):
    """
    Same as ThreadPoolExecutor, but doesn't start immediately.

    Context manager. On exit, cancels all futures.

    Also does stuff with events.
    """
    # Note that this reaches through all kinds of internals, but they're pretty stable
    _started = 0
    _finished = 0

    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)
        self._actual_max_workers = self._max_workers
        self._max_workers = 0

        if hasattr(queue, 'SimpleQueue'):  # 3.7
            self._event_queue = queue.SimpleQueue()
        else:
            self._event_queue = queue.Queue()

    def __enter__(self):
        self._max_workers = self._actual_max_workers
        self._adjust_thread_count()
        return self

    def __exit__(self, *exc):
        if sys.version_info >= (3, 9):
            self.shutdown(wait=False, cancel_futures=True)
        else:
            import queue
            # Backport of 3.9 future cancelling code
            while True:
                try:
                    work_item = self._work_queue.get_nowait()
                except queue.Empty:
                    break
                if work_item is not None:
                    work_item.future.cancel()

            self.shutdown(wait=False)

    def submit(self, fn, *args, _asset=None, **kwargs):
        if _asset is not None:
            self._started += 1

        fut = super().submit(fn, *args, **kwargs)

        if _asset is not None:
            fut.__asset = weakref.ref(_asset)
            fut.add_done_callback(self._finish)

        return fut

    def _finish(self, fut):
        asset = fut.__asset()
        if asset is not None:
            self._finished += 1
            self._event_queue.put(events.AssetLoaded(
                asset=asset,
                total_loaded=self._finished,
                total_queued=self._started - self._finished,
            ))

    def queued_events(self):
        while True:
            try:
                yield self._event_queue.get_nowait()
            except queue.Empty:
                break


_executor = DelayedThreadExecutor()


class AbstractAsset(abc.ABC):
    """
    The asset interface.

    This defines the common interface for virtual assets, proxy assets, and
    real/file assets.
    """
    @abc.abstractmethod
    def load(self):
        """
        Get the data of this asset, in the appropriate form.
        """

    def is_loaded(self):
        """
        Returns if the data is ready now or if :py:meth:`load()` will block.
        """
        return True


_asset_cache = weakref.WeakValueDictionary()


class Asset(AbstractAsset):
    """
    A resource to be loaded from the filesystem and used.

    Meant to be subclassed, but in specific ways.
    """
    _data = None

    def __new__(cls, name):
        clsname = f"{cls.__module__}:{cls.__qualname__}"
        try:
            return _asset_cache[(clsname, name)]
        except KeyError:
            inst = super().__new__(cls)
            _asset_cache[(clsname, name)] = inst
            return inst

    def __init__(self, name):
        self.name = str(name)
        self._finished = threading.Event()
        _hint(self.name, self._finished_background)

    def __repr__(self):
        return f"<{type(self).__name__} name={self.name!r}{' loaded' if self.is_loaded() else ''}>"

    def _finished_background(self, fut):
        # Internal
        # Called in background thread
        try:
            try:
                raw = fut.result()
            except FileNotFoundError:
                if hasattr(self, 'file_missing'):
                    logger.warning("File not found: %r", self.name)
                    self._data = self.file_missing()
                else:
                    raise
            else:
                self._data = self.background_parse(raw)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            # Save unhandled exceptions to be raised in the main thread
            self._raise_error = exc
        finally:
            # This always needs to happen so the main thread isn't just blocked
            self._finished.set()

    def background_parse(self, data: bytes):
        """
        Takes the data loaded from the file and returns the parsed data.

        Subclasses probably want to override this.

        Called in the background thread.
        """
        return data

    def free(self, object):
        """
        Called by :py:meth:`__del__()` if the data was loaded.

        Meant to free any resources held outside of Python.
        """

    def __del__(self):
        # This should only be called after the background threads and other
        # processing has finished.
        if self._data is not None:
            self.free(self._data)

    def is_loaded(self):
        """
        Returns if the data has been loaded and parsed.
        """
        return self._finished.is_set()

    def load(self, timeout: float = None):
        """
        Gets the parsed data.

        Will block until the data is loaded.
        """
        # FIXME
        # if _hint is _default_hint:
        #     logger.warning(f"Waited on {self!r} before the engine began")
        self._finished.wait(timeout)
        if hasattr(self, '_raise_error'):
            raise self._raise_error
        else:
            return self._data


def force_background_thread(func, *pargs, **kwargs):
    """
    Calls the given function from not the main thread.

    If already not the main thread, calls it syncronously.

    If this is the main thread, creates a new thread to call it.
    """
    if threading.current_thread() is threading.main_thread():
        t = threading.Thread(target=func, args=pargs, kwargs=kwargs, daemon=True)
        t.start()
    else:
        func(*pargs, **kwargs)


class AssetLoadingSystem(System):
    def __init__(self, *, engine, **_):
        super().__init__(**_)
        self.engine = engine

        self._event_queue = collections.deque()

    def __enter__(self):
        global _executor
        _executor.__enter__()

    def __exit__(self, *exc):
        global _executor, _asset_cache
        # Clean everything out
        _executor.__exit__(*exc)
        _asset_cache.clear()
        _executor = DelayedThreadExecutor()

    def on_idle(self, event, signal):
        for event in _executor.queued_events():
            signal(event)


def _load(filename):
    with vfs.open(filename) as file:
        return file.read()


def _hint(filename, callback=None):
    # Nothing is currently loading this data, make a fresh job
    fut = _executor.submit(_load, filename)
    if callback is not None:
        # There are circumstances where Future will call back syncronously.
        # In which case, redirect to a fresh background thread.
        fut.add_done_callback(partial(force_background_thread, callback))
