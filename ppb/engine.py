from collections import defaultdict
from collections import deque
from contextlib import ExitStack
from itertools import chain
import logging
import time
from typing import Callable
from typing import Type

from ppb.abc import Engine
from ppb.events import EventMixin
from ppb.events import Quit
from ppb.systems import PygameEventPoller
from ppb.systems import PygameMouseSystem
from ppb.systems import Renderer
from ppb.systems import Updater


class GameEngine(Engine, EventMixin):

    def __init__(self, first_scene: Type, *, log_level=logging.WARNING,
                 systems=(Renderer, Updater, PygameEventPoller, PygameMouseSystem),
                 scene_kwargs=None, **kwargs):

        super(GameEngine, self).__init__()

        # Engine Configuration
        self.log_level = log_level
        self.first_scene = first_scene
        self.scene_kwargs = scene_kwargs or {}
        self.kwargs = kwargs
        logging.basicConfig(level=self.log_level)

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
        logging.getLogger(self.__class__.__name__).info("Entering context.")
        self.start_systems()
        self.entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.getLogger(self.__class__.__name__).info("Exiting context")
        self.entered = False
        self.exit_stack.close()

    def start_systems(self):
        if self.systems:
            return
        for system in self.systems_classes:
            try:
                system = system(engine=self, **self.kwargs)
            except TypeError as e:
                if hasattr(system, "__exit__"):
                    raise e
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
        event.scene = self.current_scene
        for attr_name, attr_value in self.event_extensions[type(event)].items():
            setattr(event, attr_name, attr_value)
        for entity in chain((self,), self.systems, (self.current_scene,), self.current_scene):
            entity.__event__(event, self.signal)

    def manage_scene(self):
        if self.current_scene is None:
            self.running = False
            return None
        scene_running, next_scene = self.current_scene.change()
        if not scene_running:
            self.scenes.pop()
        if next_scene:
            self.activate(next_scene)

    def on_quit(self, quit_event: 'Quit', signal: Callable):  #TODO: Look up syntax for Callable typing.
        self.running = False

    def register(self, event_type, attribute, value):
        self.event_extensions[event_type][attribute] = value
