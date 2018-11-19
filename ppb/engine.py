from collections import defaultdict
from collections import deque
from contextlib import ExitStack
import time
from typing import Any
from typing import Callable
from typing import Type

import ppb.events as events
from ppb.abc import Engine
from ppb.events import StartScene
from ppb.events import EventMixin
from ppb.events import Quit
from ppb.systems import PygameEventPoller
from ppb.systems import Renderer
from ppb.systems import Updater
from ppb.utils import LoggingMixin


class GameEngine(Engine, EventMixin, LoggingMixin):

    def __init__(self, first_scene: Type, *,
                 systems=(Renderer, Updater, PygameEventPoller),
                 scene_kwargs=None, **kwargs):

        super(GameEngine, self).__init__()

        # Engine Configuration
        self.first_scene = first_scene
        self.scene_kwargs = scene_kwargs or {}
        self.kwargs = kwargs

        # Engine State
        self.scenes = []
        self.events = deque()
        self.event_extensions = defaultdict(dict)
        self.running = False
        self.entered = False

        # Systems
        self.systems_classes = systems
        self.systems = []
        self.exit_stack = ExitStack()

    @property
    def current_scene(self):
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
        if self.systems:
            return
        for system in self.systems_classes:
            if isinstance(system, type):
                system = system(engine=self, **self.kwargs)
            self.systems.append(system)
            self.exit_stack.enter_context(system)

    def run(self):
        if not self.entered:
            with self:
                self.start()
                self.main_loop()
        else:
            self.start()
            self.main_loop()

    def start(self):
        self.running = True
        self.activate({"scene_class": self.first_scene,
                       "kwargs": self.scene_kwargs})

    def main_loop(self):
        while self.running:
            time.sleep(0)
            for system in self.systems:
                for event in system.activate(self):
                    self.signal(event)
                    while self.events:
                        self.publish()
            self.manage_scene()

    def activate(self, next_scene: dict):
        scene = next_scene["scene_class"]
        if scene is None:
            return
        args = next_scene.get("args", [])
        kwargs = next_scene.get("kwargs", {})
        self.scenes.append(scene(self, *args, **kwargs))

    def signal(self, event):
        self.events.append(event)

    def publish(self):
        event = self.events.popleft()
        scene = self.current_scene
        event.scene = scene
        for attr_name, attr_value in self.event_extensions[type(event)].items():
            setattr(event, attr_name, attr_value)
        self.__event__(event, self.signal)
        for system in self.systems:
            system.__event__(event, self.signal)
        # Required for if we publish with no current scene.
        # Should only happen when the last scene stops via event.
        if scene is not None:
            scene.__event__(event, self.signal)
            for game_object in scene:
                game_object.__event__(event, self.signal)

    def manage_scene(self):
        if self.current_scene is None:
            self.running = False
            return None
        scene_running, next_scene = self.current_scene.change()
        if not scene_running:
            self.scenes.pop()
        if next_scene:
            self.activate(next_scene)

    def on_start_scene(self, event: StartScene, signal: Callable[[Any], None]):
        """
        Start a new scene. The current scene pauses.
        """
        self.pause_scene()
        self.start_scene(event.new_scene, event.kwargs)

    def on_stop_scene(self, event: events.StopScene, signal: Callable[[Any], None]):
        """
        Stop a running scene. If there's a scene on the stack, it resumes.
        """
        self.stop_scene()
        if self.current_scene is not None:
            signal(events.SceneContinued())
        else:
            signal(events.Quit())

    def on_replace_scene(self, event: events.ReplaceScene, signal):
        """
        Replace the running scene with a new one.
        """
        self.stop_scene()
        self.start_scene(event.new_scene, event.kwargs)

    def on_quit(self, quit_event: Quit, signal: Callable[[Any], None]):
        self.running = False

    def pause_scene(self):
        # Empty the queue before changing scenes.
        self.flush_events()
        self.signal(events.ScenePaused())
        self.publish()

    def stop_scene(self):
        # Empty the queue before changing scenes.
        self.flush_events()
        self.signal(events.SceneStopped())
        self.publish()
        self.scenes.pop()

    def start_scene(self, scene, kwargs):
        if kwargs:
            scene = scene(self, **kwargs)
        self.scenes.append(scene)
        self.signal(events.SceneStarted())

    def register(self, event_type, attribute, value):
        self.event_extensions[event_type][attribute] = value

    def flush_events(self):
        """
        Flush the event queue.

        Call before doing anything that will cause signals to be delivered to
        the wrong scene.
        """
        self.events = deque()