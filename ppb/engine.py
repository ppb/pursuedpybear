import logging
import time
from typing import Type
import pygame
from ppb.abc import Engine, Scene
from .events import EventSystem


class GameEngine(Engine):

    def __init__(self, first_scene: Type, *, delta_time=0.016, resolution=(600, 400), flags=0, depth=0, log_level=logging.WARNING, **kwargs):
        super(GameEngine, self).__init__()

        # Engine Configuration
        self.delta_time = delta_time
        self.resolution = resolution
        self.flags = flags
        self.depth = depth
        self.log_level = log_level
        self.first_scene = first_scene
        logging.basicConfig(level=self.log_level)

        # Engine State
        self.scenes = []
        self.unused_time = 0
        self.last_tick = None
        self.running = False
        self.display = None

        self.event_engine = EventSystem()

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
        if hasattr(self.current_scene, "background") and self.current_scene is not None:
            self.display.blit(self.current_scene.background, (0, 0, 0, 0))
        else:
            self.display.fill(self.current_scene.background_color)

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

    def fire_event(self, name: str, bag: object, scene: Scene=None):
        """
        Fire an event, executing its handlers.
        """
        if scene is None:
            scene = self.current_scene

        self.event_engine.fire_event(name, bag, scene)
