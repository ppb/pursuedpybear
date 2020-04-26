"""
The asset loading system.
"""
import abc
import collections
import concurrent.futures
import logging
import queue
import sys
import threading
import weakref

import ppb.vfs as vfs
import ppb.events as events
from ppb.systemslib import System

__all__ = (
    'AssetLoadingSystem',
    'AbstractAsset', 'BackgroundMixin', 'ChainingMixin', 'FreeingMixin',
    'Asset',
)

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

    def running(self):
        return (self._max_workers > 0) and (not self._shutdown)

    def submit(self, fn, *args, _asset=None, **kwargs):
        if _asset is not None:
            self._started += 1

        fut = super().submit(fn, *args, **kwargs)

        if _asset is not None:
            fut.__asset = weakref.ref(_asset)
            fut.add_done_callback(self._finish)

        return fut

    def gather(self, futures, callback, *pargs, **kwargs):
        mock = MockFuture()

        def waiter():
            done, not_done = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_EXCEPTION)
            for f in done:
                exc = f.exception()
                if exc is not None:
                    mock.set_exception(exc)
                    break
            else:
                assert not not_done
                newfut = self.submit(callback, *pargs, **kwargs)
                mock.handoff(newfut)

        threading.Thread(target=waiter).start()

        return mock

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


class MockFuture(concurrent.futures.Future):
    """
    Acts as a Future's understudy until the real future is availalble.
    """
    _handed_off = False

    def handoff(self, fut):
        """
        Gives our state to the real future
        """
        with self._condition:
            if self._handed_off:
                raise concurrent.futures.InvalidStateError(f"{self!r} already handed off")
            self._handed_off = True

            # Add the callbacks
        with self._condition:
            callbacks, self._done_callbacks = self._done_callbacks, []

        for fn in callbacks:
            fut.add_done_callback(fn)

        # Apply cancellation
        if self.cancelled():
            fut.cancel()
        else:
            fut.add_done_callback(self._pass_on_result)

    def _pass_on_result(self, fut):
        try:
            result = fut.result()
        except BaseException as exc:
            self.set_exception(exc)
        else:
            self.set_result(result)


class AbstractAsset(abc.ABC):
    """
    The asset interface.

    This defines the common interface for virtual assets, proxy assets, and
    real/file assets.
    """
    @abc.abstractmethod
    def load(self, timeout: float = None):
        """
        Get the data of this asset, in the appropriate form.
        """

    def is_loaded(self):
        """
        Returns if the data is ready now or if :py:meth:`load()` will block.
        """
        return True


class BackgroundMixin:
    """
    Asset that does stuff in the background.
    """
    _future = None

    def _start(self):
        """
        Queue the background stuff to run.

        Call at the end of __init__().
        """
        self._future = _executor.submit(self._background, _asset=self)

    def _background(self):
        """
        The background processing.

        Override me.
        """

    def is_loaded(self):
        """
        Returns if the data has been loaded and parsed.
        """
        return self._future is not None and self._future.done()

    def load(self, timeout: float = None):
        """
        Gets the parsed data.

        Will block until the data is loaded.
        """
        # NOTE: This is called by FreeingMixin.__del__()
        if not self.is_loaded() and not _executor.running():
            logger.warning(f"Waited on {self!r} outside of the engine")
        return self._future.result(timeout)


class ChainingMixin(BackgroundMixin):
    """
    Asset that does stuff in the background, after other assets have loaded.
    """
    def _start(self, *assets):
        """
        Queue the background stuff to run.

        Call at the end of __init__().
        """
        self._future = _executor.gather([
            asset._future
            for asset in assets
            if hasattr(asset, '_future')
        ], self._background, _asset=self)


class FreeingMixin:
    """
    Asset that supports freeing
    """
    def free(self, object):
        """
        Called by :py:meth:`__del__()` if the data was loaded.

        Meant to free any resources held outside of Python.
        """

    def __del__(self):
        # This should only be called after the background threads and other
        # processing has finished.
        # NOTE: This isn't super great, but there isn't a better way without
        # knowing what we've been mixed with.
        if self.is_loaded():
            try:
                data = self.load()
            except BaseException:
                pass
            else:
                self.free(data)


_asset_cache = weakref.WeakValueDictionary()


class Asset(BackgroundMixin, FreeingMixin, AbstractAsset):
    """
    A resource to be loaded from the filesystem and used.

    Meant to be subclassed, but in specific ways.
    """
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
        self._start()

    def __repr__(self):
        return f"<{type(self).__name__} name={self.name!r}{' loaded' if self.is_loaded() else ''} at 0x{id(self):x}>"

    def _background(self):
        # Called in background thread
        try:
            file = vfs.open(self.name)
        except FileNotFoundError:
            if hasattr(self, 'file_missing'):
                logger.warning("File not found: %r", self.name)
                return self.file_missing()
            else:
                raise
        else:
            with file:
                raw = file.read()
            return self.background_parse(raw)

    def background_parse(self, data: bytes):
        """
        Takes the data loaded from the file and returns the parsed data.

        Subclasses probably want to override this.

        Called in the background thread.
        """
        return data


class AssetLoadingSystem(System):
    """
    Connects the asset system to PPB, managing lifecycles and such.

    To minimize the chance of a race condition around initialization, place at
    the end of the list of systems.
    """
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
