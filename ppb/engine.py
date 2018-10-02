from collections import defaultdict, deque
from contextlib import ExitStack
from itertools import chain
import time
from typing import Callable, Type

import pyglet

from ppb.abc import Engine
from ppb.events import EventMixin, Quit
from ppb.systems import Updater, PygletWindow
from ppb.utils import LoggingMixin


class GameEngine(
    EventMixin, LoggingMixin,
    pyglet.app.EventLoop,
    Engine
):

    def __init__(self, first_scene: Type, *,
                 systems=(Updater, PygletWindow),
                 scene_kwargs=None, **kwargs):

        super().__init__()

        # Engine Configuration
        self.first_scene = first_scene
        self.scene_kwargs = scene_kwargs or {}
        self.kwargs = kwargs

        # Engine State
        self.scenes = []
        self.event_extensions = defaultdict(dict)

        # Systems
        self.systems_classes = systems
        self.systems = []
        self.exit_stack = ExitStack()

    @property
    def running(self):
        return not self.has_exit
    

    # pyglet event
    def on_enter(self):
        self.logger.info("Entering context")
        self.start_systems()
        self.activate({"scene_class": self.first_scene,
                       "kwargs": self.scene_kwargs})

    # pyglet event
    def on_exit(self):
        self.logger.info("Exiting context")
        self.exit_stack.close()

    def start_systems(self):
        if self.systems:
            return
        for system in self.systems_classes:
            if isinstance(system, type):
                system = system(engine=self, **self.kwargs)
            self.systems.append(system)
            self.exit_stack.enter_context(system)

    # override EventLoop
    def idle(self):
        for system in self.systems:
            for event in system.activate(self):
                self.signal(event)
        self.manage_scene()
        return super().idle()

    @property
    def current_scene(self):
        try:
            return self.scenes[-1]
        except IndexError:
            return None

    def activate(self, next_scene: dict):
        scene = next_scene["scene_class"]
        if scene is None:
            return
        args = next_scene.get("args", [])
        kwargs = next_scene.get("kwargs", {})
        self.scenes.append(scene(self, *args, **kwargs))

    def manage_scene(self):
        if self.current_scene is None:
            self.exit()
            return None
        scene_running, next_scene = self.current_scene.change()
        if not scene_running:
            self.scenes.pop()
        if next_scene:
            self.activate(next_scene)

    def signal(self, event):
        event.scene = self.current_scene
        for attr_name, attr_value in self.event_extensions[type(event)].items():
            setattr(event, attr_name, attr_value)
        pyglet.app.platform_event_loop.post_event(self, '_on_ppb_event', event)

    # Pyglet Event
    def _on_ppb_event(self, event):
        for entity in chain((self,), self.systems, (self.current_scene,), self.current_scene):
            entity.__event__(event, self.signal)

    # PPB event
    def on_quit(self, quit_event: 'Quit', signal: Callable):  #TODO: Look up syntax for Callable typing.
        self.exit()

    def register(self, event_type, attribute, value):
        self.event_extensions[event_type][attribute] = value


GameEngine.register_event_type('_on_ppb_event')
