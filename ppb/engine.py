import time
from collections import defaultdict
from collections import deque
from contextlib import ExitStack
from itertools import chain
from typing import Any
from typing import Callable
from typing import DefaultDict
from typing import Hashable
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Type
from typing import Union

import ppb
import ppb.systemslib
from ppb import events
from ppb.assetlib import AssetLoadingSystem
from ppb.gomlib import Children, GameObject
from ppb.gomlib import walk
from ppb.errors import BadChildException
from ppb.errors import BadEventHandlerException
from ppb.scenes import BaseScene
from ppb.systems import EventPoller
from ppb.systems import Renderer
from ppb.systems import SoundController
from ppb.systems import Updater
from ppb.utils import LoggingMixin
from ppb.utils import camel_to_snake
from ppb.utils import get_time

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


class EngineChildren(Children):
    """
    Acts as a Children collection for engines:

    * Scenes are managed in their own stack
    * Systems have context managers
    * Manipulating Scenes must be through pushing and popping
    * Manipulating Systems is disallowed while the engine is running.
    * Only the active (topmost) Scene is exposed as a child
    * The iteration order is defined as: Systems, Current Scene, anything else
    """
    entered: bool

    def __init__(self):
        super().__init__()
        self._scenes = []
        self._systems = set()

        self._stack = ExitStack()
        self.entered = False

    def __contains__(self, item: Hashable) -> bool:
        return (
            item in self._all or
            item in self._scenes or
            item in self._systems
        )

    def __iter__(self) -> Iterator[Hashable]:
        yield from self._systems
        if self._scenes:
            yield self._scenes[-1]
        yield from self._all

    def __len__(self) -> int:
        return len(self._all)

    @property
    def current_scene(self):
        """
        The top of the scene stack.

        :return: The currently running scene.
        :rtype: ppb.BaseScene
        """
        try:
            return self._scenes[-1]
        except IndexError:
            return None

    def add(self, child: Hashable, tags: Iterable[Hashable] = ()) -> Hashable:
        """
        Add a child.

        :param child: Any Hashable object. The item to be added.
        :param tags: An iterable of Hashable objects. Values that can be used to
              retrieve a group containing the child.

        Note that Scenes and Systems have special restrictions.

        Examples: ::

            children.add(MyObject())

            children.add(MyObject(), tags=("red", "blue")
        """
        # Ugh, this is a copy of the implementation in Children.
        if isinstance(child, type):
            raise BadChildException(child)

        if isinstance(tags, (str, bytes)):
            raise TypeError("You passed a string instead of an iterable, this probably isn't what you intended.\n\nTry making it a tuple.")

        if isinstance(child, ppb.BaseScene):
            raise TypeError("Scenes must be pushed, not added. You probably want the StartScene or ReplaceScene events.")
        elif isinstance(child, ppb.systemslib.System):
            if self.entered:
                raise RuntimeError("Systems cannot be added while the engine is running")
            self._systems.add(child)
        else:
            self._all.add(child)

        for kind in type(child).mro():
            self._kinds[kind].add(child)
        for tag in tags:
            self._tags[tag].add(child)

        return child

    def remove(self, child: Hashable) -> Hashable:
        """
        Remove the given object from the container.

        Note that Scenes and Systems have special restrictions.

        :param child: A hashable contained by container.

        Example: ::

            container.remove(myObject)
        """
        # Ugh, this is a copy of the implementation in Children.
        if isinstance(child, ppb.BaseScene):
            raise TypeError("Scenes must be popped, not removed. You probably want the StopScene event.")
        elif isinstance(child, ppb.systemslib.System):
            if self.entered:
                raise RuntimeError("Systems cannot be removed while the engine is running")
            self._systems.remove(child)
        else:
            self._all.remove(child)

        for kind in type(child).mro():
            self._kinds[kind].remove(child)
        for s in self._tags.values():
            s.discard(child)

        return child

    def push_scene(self, scene):
        """
        Push a scene onto the scene stack.

        If you are not an Engine, you probably don't want to call this.
        """
        self._scenes.append(scene)

        for kind in type(scene).mro():
            self._kinds[kind].add(scene)

    def pop_scene(self):
        """
        Pop a scene from the scene stack.

        If you are not an Engine, you probably don't want to call this.
        """
        child = self._scenes.pop()
        for kind in type(child).mro():
            self._kinds[kind].remove(child)
        for s in self._tags.values():
            s.discard(child)

    def __enter__(self):
        assert not self.entered
        self.entered = True
        try:
            for system in self._systems:
                self._stack.enter_context(system)
        except:  # noqa
            self._stack.close()
            self.entered = False
            raise

    def __exit__(self, *exc):
        self._stack.close()
        self.entered = False

    def has_systems(self):
        """
        Shortcut for Engines to know if they've added any Systems.
        """
        return bool(self._systems)


class GameEngine(GameObject, LoggingMixin):
    """
    The core component of :mod:`ppb`.

    To use the engine directly, treat it as a context manager: ::

       with GameEngine(BaseScene, **kwargs) as ge:
           ge.run()
    """
    def __init__(self, first_scene: Union[Type, BaseScene], *,
                 basic_systems=(Renderer, Updater, EventPoller, SoundController, AssetLoadingSystem),
                 systems=(), scene_kwargs=None, **kwargs):
        """
        :param first_scene: A :class:`~ppb.BaseScene` type.
        :type first_scene: Union[Type, scenes.BaseScene]
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

        super().__init__()  # FIXME: This is breaking the GameObject protocol
        self.children = EngineChildren()

        # Engine Configuration
        self.first_scene = first_scene
        self.scene_kwargs = scene_kwargs or {}
        self.kwargs = kwargs

        # Engine State
        self.events = deque()
        self.event_extensions: DefaultDict[Union[Type, _ellipsis], List[Callable[[Any], None]]] = defaultdict(list)
        self.entered = False
        self.running = False
        self._last_idle_time = None

        # Systems
        self.systems_classes = list(chain(basic_systems, systems))

    @property
    def current_scene(self):
        """
        The top of the scene stack.

        :return: The currently running scene.
        :rtype: ppb.BaseScene
        """
        return self.children.current_scene

    def __enter__(self):
        self.logger.info("Entering context")
        self.start_systems()
        self.children.__enter__()
        self.entered = True
        return self

    def __exit__(self, *exc):
        self.logger.info("Exiting context")
        self.entered = False
        self.children.__exit__(*exc)

    def start_systems(self):
        """Initialize the systems."""
        if self.children.has_systems():
            return
        for system in self.systems_classes:
            if isinstance(system, type):
                system = system(engine=self, **self.kwargs)
            self.children.add(system)

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
        self._last_idle_time = get_time()
        if isinstance(self.first_scene, type):
            scene = self.first_scene(**self.scene_kwargs)
        else:
            scene = self.first_scene

        self._start_scene(scene, None)

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
        now = get_time()
        self.signal(events.Idle(now - self._last_idle_time))
        self._last_idle_time = now
        while self.events:
            self.publish()

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
        for obj in walk(self):
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

    def signal(self, event):
        """
        Add an event to the event queue.

        Thread-safe.

        You will rarely call this directly from a :class:`GameEngine` instance.
        The current :class:`GameEngine` instance will pass it's signal method
        as part of publishing an event.
        """
        self.events.append(event)

    def _flush_events(self):
        """
        Flush the event queue.

        Call before doing anything that will cause signals to be delivered to
        the wrong scene.
        """
        self.events = deque()

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
        self.children.pop_scene()

    def _start_scene(self, scene, kwargs):
        """Start a scene."""
        if isinstance(scene, type):
            scene = scene(**(kwargs or {}))
        self.children.push_scene(scene)
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
