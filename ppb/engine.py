import logging
import time
from typing import Type
import pygame
from ppb.abc import Engine, Scene


class GameEngine(Engine):

    def __init__(self, first_scene: Type, **kwargs):
        super(GameEngine, self).__init__()

        # Engine Configuration
        self.delta_time = kwargs.get("delta_time", 0.016)
        self.resolution = kwargs.get("resolution", (600, 400))
        self.flags = kwargs.get("flags", 0)
        self.depth = kwargs.get("depth", 0)
        self.log_level = kwargs.get("log_level", logging.WARNING)
        self.first_scene = first_scene
        logging.basicConfig(level=self.log_level)

        # Engine State
        self.scenes = []
        self.unused_time = 0
        self.last_tick = None
        self.running = False
        self.display = None

    def __enter__(self):
        logging.getLogger(self.__class__.__name__).info("Entering context.")
        pygame.init()
        self.display = pygame.display.set_mode(self.resolution,
                                               self.flags,
                                               self.depth)
        self.update_input()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.getLogger(self.__class__.__name__).info("Exiting context")
        pygame.quit()

    def start(self):
        self.running = True
        self.last_tick = time.time()
        self.activate({"scene_class": self.first_scene})

    def manage_scene(self, scene_running, next_scene):
        if not scene_running:
            self.scenes.pop()
        if next_scene:
            self.activate(next_scene)

    def run(self):
        self.start()
        while self.running:
            time.sleep(.0000000001)
            scene = self.current_scene
            if scene is None:
                return
            self.manage_scene(*scene.change())
            pygame.display.update(list(scene.render()))
            tick = time.time()
            self.unused_time += tick - self.last_tick
            self.last_tick = tick
            while self.unused_time >= self.delta_time:
                for event in pygame.event.get():
                    scene.handle_event(event)
                    if event.type == pygame.QUIT:
                        return
                self.update_input()
                scene.simulate(self.delta_time)
                self.unused_time -= self.delta_time

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
        args = next_scene.get("arguments", [])
        kwargs = next_scene.get("keyword_arguments", {})
        self.scenes.append(scene(self, *args, **kwargs))

    def update_input(self):
        self.mouse["x"], self.mouse["y"] = pygame.mouse.get_pos()
        self.mouse[1], self.mouse[2], self.mouse[3] = pygame.mouse.get_pressed()
