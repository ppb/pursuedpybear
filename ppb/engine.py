import logging
import time
from typing import Type
import pygame

from ppb.abc import Engine
from ppb.systems import Renderer


class GameEngine(Engine):

    def __init__(self, first_scene: Type, *, delta_time=0.016, depth=0,
                 flags=0, log_level=logging.WARNING, renderer_class=Renderer,
                 resolution=(600, 400), scene_kwargs=None, **kwargs):

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
        self.unused_time = 0
        self.last_tick = None
        self.running = False

        # Systems
        self.renderer = renderer_class()

    def __enter__(self):
        logging.getLogger(self.__class__.__name__).info("Entering context.")
        pygame.init()
        pygame.display.set_mode(self.resolution, self.flags, self.depth)
        self.update_input()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.getLogger(self.__class__.__name__).info("Exiting context")
        pygame.quit()

    def start(self):
        self.running = True
        self.last_tick = time.time()
        self.activate({"scene_class": self.first_scene,
                       "kwargs": self.scene_kwargs})
        self.renderer.start()

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
            self.render()
            self.advance_time()
            while self.unused_time >= self.delta_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                self.update_input()
                self.current_scene.simulate(self.delta_time)
                self.unused_time -= self.delta_time
            self.manage_scene()

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

    def update_input(self):
        self.mouse["x"], self.mouse["y"] = pygame.mouse.get_pos()
        self.mouse[1], self.mouse[2], self.mouse[3] = pygame.mouse.get_pressed()

    def render(self):
        self.renderer.render(self.current_scene)

    def advance_time(self):
        tick = time.time()
        self.unused_time += tick - self.last_tick
        self.last_tick = tick
