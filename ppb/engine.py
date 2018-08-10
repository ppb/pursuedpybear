from collections import deque
from contextlib import ExitStack
from itertools import chain
import logging
import time
from typing import Callable
from typing import Type
import pygame

from ppb.abc import Engine
from ppb.events import EventMixin
from ppb.events import Quit
from ppb.systems import Renderer
from ppb.systems import Updater


class GameEngine(Engine, EventMixin):

    def __init__(self, first_scene: Type, *, delta_time: float=0.016,
                 depth: int=0, flags=0, log_level=logging.WARNING,
                 systems=(Renderer, Updater), resolution=(600, 400),
                 scene_kwargs=None, **kwargs):

        super(GameEngine, self).__init__()

        # Engine Configuration
        self.delta_time = delta_time
        self.resolution = resolution
        self.flags = flags
        self.depth = depth
        self.log_level = log_level
        self.first_scene = first_scene
        self.scene_kwargs = scene_kwargs or {}
        logging.basicConfig(level=self.log_level)

        # Engine State
        self.scenes = []
        self.events = deque()
        self.unused_time = 0
        self.last_tick = None
        self.running = False

        # Systems
        self.systems_classes = systems
        self.systems = []
        self.exit_stack = ExitStack()

    def __enter__(self):
        logging.getLogger(self.__class__.__name__).info("Entering context.")
        pygame.init()
        pygame.display.set_mode(self.resolution, self.flags, self.depth)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.getLogger(self.__class__.__name__).info("Exiting context")
        pygame.quit()

    def start(self):
        self.running = True
        self.last_tick = time.time()
        self.activate({"scene_class": self.first_scene,
                       "kwargs": self.scene_kwargs})
        self.start_systems()

    def start_systems(self):
        for system in self.systems_classes:
            try:
                system = system()
            except : # TODO: Check if type error or attribute error
                pass
            self.systems.append(system)
            self.exit_stack.enter_context(system)

    def manage_scene(self):
        if self.current_scene is None:
            self.running = False
            return None
        scene_running, next_scene = self.current_scene.change()
        if not scene_running:
            self.scenes.pop()
        if next_scene:
            self.activate(next_scene)

    def run(self):
        self.start()
        while self.running:
            time.sleep(.0000000001)
            self.advance_time()
            while self.unused_time >= self.delta_time:
                for system in self.systems:
                    logging.warning(f"System: {system}")
                    for event in system.activate(self):
                        self.signal(event)
                        while self.events:
                            self.publish()
                self.unused_time -= self.delta_time
            self.manage_scene()
        self.exit_stack.close()

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

    def advance_time(self):
        tick = time.time()
        self.unused_time += tick - self.last_tick
        self.last_tick = tick

    def publish(self):
        event = self.events.popleft()
        event.scene = self.current_scene
        for entity in chain((self,), self.systems, (self.current_scene,), self.current_scene):
            entity.__event__(event, self.signal)

    def signal(self, event):
        self.events.append(event)

    def on_quit(self, quit_event: 'Quit', signal: Callable):  #TODO: Look up syntax for Callable typing.
        self.running = False
