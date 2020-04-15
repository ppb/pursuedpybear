import time
from collections import defaultdict
from collections import deque
from contextlib import ExitStack
from itertools import chain
from typing import Any
from typing import Callable
from typing import DefaultDict
from typing import List
from typing import Type
from typing import Union

from ppb import events
from ppb.assetlib import AssetLoadingSystem
from ppb.errors import BadEventHandlerException
from ppb.systems import EventPoller
from ppb.systems import Renderer
from ppb.systems import SoundController
from ppb.systems import Updater
from ppb.utils import LoggingMixin
from ppb.utils import camel_to_snake

_ellipsis = type(...)

_cached_handler_names = {}


def _get_handler_name(txt):
    result = _cached_handler_names.get(txt)
    if result is None:
        result = "on_" + camel_to_snake(txt)
        _cached_handler_names[txt] = result
    return result


for x in events.__all__:
    _get_handler_name(x)


class GameEngine(LoggingMixin):
    """
    The core component of :mod:`ppb`.

    To use the engine directly, treat it as a context manager: ::

       with GameEngine(BaseScene, **kwargs) as ge:
           ge.run()
    """
    def __init__(self, first_scene: Type, *,
                 basic_systems=(Renderer, Updater, EventPoller, SoundController, AssetLoadingSystem),
                 systems=(), scene_kwargs=None, **kwargs):
        """
        :param first_scene: A :class:`~ppb.BaseScene` type.
        :type first_scene: Type
        :param basic_systems: :class:systemslib.Systems that are considered
           the "default". Includes: :class:`~systems.Renderer`,
           :class:`~systems.Updater`, :class:`~systems.EventPoller`,
           :class:`~systems.SoundController`, :class:`~systems.AssetLoadingSystem`.
        :type basic_systems: Iterable[systemslib.System]
        :param systems: Additional user defined systems.
        :type systems: Iterable[systemslib.System]
        :param scene_kwargs: Keyword arguments passed along to the first scene.
        :type scene_kwargs: Dict[str, Any]
        :param kwargs: Additional keyword arguments. Passed to the systems.

        .. warning::
           Passing in your own ``basic_systems`` can have unintended
           consequences. Consider passing via systems parameter instead.
        """

        super(GameEngine, self).__init__()

        # Engine Configuration
        self.first_scene = first_scene
        self.scene_kwargs = scene_kwargs or {}
        self.kwargs = kwargs

        # Engine State
        self.scenes = []
        self.events = deque()
        self.event_extensions: DefaultDict[Union[Type, _ellipsis], List[Callable[[Any], None]]] = defaultdict(list)
        self.running = False
        self.entered = False
        self._last_idle_time = None

        # Systems
        self.systems_classes = list(chain(basic_systems, systems))
        self.systems = []
        self.exit_stack = ExitStack()

    @property
    def current_scene(self):
        """
        The top of the scene stack.

        :return: The currently running scene.
        :rtype: ppb.BaseScene
        """
        try:
            return self.scenes[-1]
        except IndexError:
            return None

    def __enter__(self):
        self.logger.info("Entering context")
        self.start_systems()
        self.entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("Exiting context")
        self.entered = False
        self.exit_stack.close()

    def start_systems(self):
        """Initialize and enter the systems."""
        if self.systems:
            return
        for system in self.systems_classes:
            if isinstance(system, type):
                system = system(engine=self, **self.kwargs)
            self.systems.append(system)
            self.exit_stack.enter_context(system)

    def run(self):
        """
        Begin the main loop.

        If you have not entered the :class:`GameEngine`, this function will
        enter it for you before starting.

        Example: ::

           GameEngine(BaseScene, **kwargs).run()
        """
        if not self.entered:
            with self:
                self.start()
                self.main_loop()
        else:
            self.start()
            self.main_loop()

    def start(self):
        """
        Starts the engine.

        Called by :meth:`GameEngine.run` before :meth:`GameEngine.main_loop`.

        You shouldn't call this yourself unless you're embedding :mod:`ppb` in
        another event loop.
        """
        self.running = True
        self._last_idle_time = time.monotonic()
        self.activate({"scene_class": self.first_scene,
                       "kwargs": self.scene_kwargs})

    def main_loop(self):
        """
        Loop forever.

        If you're embedding :mod:`ppb` in an external event loop you should not
        use this method. Call :meth:`GameEngine.loop_once` instead.
        """
        while self.running:
            time.sleep(0)
            self.loop_once()

    def loop_once(self):
        """
        Iterate once.

        If you're embedding :mod:`ppb` in an external event loop call once per
        loop.
        """
        if not self.entered:
            raise ValueError("Cannot run before things have started",
                             self.entered)
        now = time.monotonic()
        self.signal(events.Idle(now - self._last_idle_time))
        self._last_idle_time = now
        while self.events:
            self.publish()

    def activate(self, next_scene: dict):
        """
        Instantiates and sets up a new scene.

        :param next_scene: A dictionary with the keys:

           * "scene_class": A :class:`~ppb.BaseScene` type.
           * "args": A :class:`list` of positional arguments.
           * "kwargs": A :class:`dict` of keyword arguments.
        """
        scene = next_scene["scene_class"]
        if scene is None:
            return
        args = next_scene.get("args", [])
        kwargs = next_scene.get("kwargs", {})
        self._start_scene(scene(*args, **kwargs), None)

    def signal(self, event):
        """
        Add an event to the event queue.

        Thread-safe.

        You will rarely call this directly from a :class:`GameEngine` instance.
        The current :class:`GameEngine` instance will pass it's signal method
        as part of publishing an event.
        """
        self.events.append(event)

    def publish(self):
        """
        Publish the next event to every object in the tree.
        """
        event = self.events.popleft()
        scene = self.current_scene
        event.scene = scene
        extensions = chain(self.event_extensions[type(event)], self.event_extensions[...])

        # Hydrating extensions.
        for callback in extensions:
            callback(event)

        event_handler_name = _get_handler_name(type(event).__name__)
        for obj in self.walk():
            method = getattr(obj, event_handler_name, None)
            if callable(method):
                try:
                    method(event, self.signal)
                except TypeError as ex:
                    from inspect import signature
                    sig = signature(method)
                    try:
                        sig.bind(event, self.signal)
                    except TypeError:
                        raise BadEventHandlerException(obj, event_handler_name, event) from ex
                    else:
                        raise

    def on_start_scene(self, event: events.StartScene, signal: Callable[[Any], None]):
        """
        Start a new scene. The current scene pauses.

        Do not call this method directly. It is called by the GameEngine when a
        :class:`~events.StartScene` event is fired.
        """
        self._pause_scene()
        self._start_scene(event.new_scene, event.kwargs)

    def on_stop_scene(self, event: events.StopScene, signal: Callable[[Any], None]):
        """
        Stop a running scene. If there's a scene on the stack, it resumes.

        Do not call this method directly. It is called by the GameEngine when a
        :class:`~events.StopScene` event is fired.
        """
        self._stop_scene()
        if self.current_scene is not None:
            signal(events.SceneContinued())
        else:
            signal(events.Quit())

    def on_replace_scene(self, event: events.ReplaceScene, signal):
        """
        Replace the running scene with a new one.

        Do not call this method directly. It is called by the GameEngine when a
        :class:`~events.ReplaceScene` event is fired.
        """
        self._stop_scene()
        self._start_scene(event.new_scene, event.kwargs)

    def on_quit(self, quit_event: events.Quit, signal: Callable[[Any], None]):
        """
        Shut down the event loop.

        Do not call this method directly. It is called by the GameEngine when a
        :class:`~events.Quit` event is fired.
        """
        self.running = False

    def _pause_scene(self):
        """Pause the current scene."""
        # Empty the queue before changing scenes.
        self._flush_events()
        self.signal(events.ScenePaused())
        self.publish()

    def _stop_scene(self):
        """Stop the current scene."""
        # Empty the queue before changing scenes.
        self._flush_events()
        self.signal(events.SceneStopped())
        self.publish()
        self.scenes.pop()

    def _start_scene(self, scene, kwargs):
        """Start a scene."""
        if isinstance(scene, type):
            scene = scene(**(kwargs or {}))
        self.scenes.append(scene)
        self.signal(events.SceneStarted())

    def register(self, event_type: Union[Type, _ellipsis], callback: Callable[[], Any]):
        """
        Register a callback to be applied to an event at time of publishing.

        Primarily to be used by subsystems.

        The callback will receive the event. Your code should modify the event
        in place. It does not need to return it.

        :param event_type: The class of an event.
        :param callback: A callable, must accept an event, and return no value.
        :return: None
        """
        if not isinstance(event_type, type) and event_type is not ...:
            raise TypeError(f"{type(self)}.register requires event_type to be a type.")
        if not callable(callback):
            raise TypeError(f"{type(self)}.register requires callback to be callable.")
        self.event_extensions[event_type].append(callback)

    def _flush_events(self):
        """
        Flush the event queue.

        Call before doing anything that will cause signals to be delivered to
        the wrong scene.
        """
        self.events = deque()

    def walk(self):
        """
        Walk the object tree.

        Publication order: The :class:`GameEngine`, the
        :class:`~ppb.systemslib.System` list, the current
        :class:`~ppb.BaseScene`, then finally the :class:`~ppb.Sprite` objects
        in the current scene.
        """
        yield self
        yield from self.systems
        yield self.current_scene
        if self.current_scene is not None:
            yield from self.current_scene
