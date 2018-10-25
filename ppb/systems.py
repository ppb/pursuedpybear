import random
import time
from typing import Union
from typing import Iterable

import pygame

import ppb.events as events
import ppb.flags as flags
import ppb.buttons as buttons
from ppb.vector import Vector

default_resolution = 800, 600


class System(events.EventMixin):

    def __init__(self, **_):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def activate(self, engine):
        return []


class PygameEventPoller(System):
    """
    An event poller that converts Pygame events into PPB events.
    """

    event_map = None

    button_map = {
        1: buttons.Primary,
        2: buttons.Tertiary,
        3: buttons.Secondary,
    }

    def __new__(cls, *args, **kwargs):
        if cls.event_map is None:
            cls.event_map = {
                pygame.QUIT: "quit",
                pygame.MOUSEMOTION: "mouse_motion",
                pygame.MOUSEBUTTONDOWN: "button_pressed",
                pygame.MOUSEBUTTONUP: "button_released",
            }
        return super().__new__(cls)

    def __init__(self, resolution=default_resolution, **kwargs):
        self.offset = Vector(-0.5 * resolution[0],
                             -0.5 * resolution[1])

    def __enter__(self):
        pygame.init()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def on_update(self, update, signal):
        for pygame_event in pygame.event.get():
            methname = self.event_map.get(pygame_event.type)
            if methname is not None:  # Is there a handler for this pygame event?
                ppbevent = getattr(self, methname)(pygame_event, update.scene)
                if ppbevent:  # Did the handler actually produce a ppb event?
                    signal(ppbevent)

    def quit(self, event, scene):
        return events.Quit()

    def mouse_motion(self, event, scene):
        screen_position = Vector(*event.pos)
        camera = scene.main_camera
        scene_position = camera.translate_to_frame(screen_position)
        delta = Vector(*event.rel) * (1/camera.pixel_ratio)
        buttons = {
            self.button_map[btn+1]
            for btn, value in enumerate(event.buttons)
            if value
        }
        return events.MouseMotion(
            position=scene_position,
            screen_position=screen_position,
            delta=delta,
            buttons=buttons)

    def button_pressed(self, event, scene):
        screen_position = Vector(*event.pos)
        camera = scene.main_camera
        scene_position = camera.translate_to_frame(screen_position)
        btn = self.button_map.get(event.button)
        if btn is not None:
            return events.ButtonPressed(
                button=btn,
                position=scene_position,
                # TODO: Add frame position
            )

    def button_released(self, event, scene):
        screen_position = Vector(*event.pos)
        camera = scene.main_camera
        scene_position = camera.translate_to_frame(screen_position)
        btn = self.button_map.get(event.button)
        if btn is not None:
            return events.ButtonReleased(
                button=btn,
                position=scene_position,
                # TODO: Add frame position
            )


class Quitter(System):
    """
    System for running test. Limits the engine to a single loop.
    """

    def __init__(self, count=1, **kwargs):
        self.counter = 0
        self.count = count

    def activate(self, engine):
        self.counter += 1
        if self.counter >= self.count:
            yield events.Quit()


class FailerSystem(System):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start = time.monotonic()
    def activate(self, engine):
        try:
            parent = engine.scenes[0]
        except IndexError:
            return ()
        if parent.count > 0 and engine.current_scene != parent:
            raise AssertionError("ParentScene should not be counting while a child exists.")
        if time.monotonic() - self.start > 1:
            raise AssertionError("Ran too long.")
        return ()


class Renderer(System):

    def __init__(self, resolution=default_resolution, window_title: str="PursuedPyBear", **kwargs):
        self.resolution = resolution
        self.resources = {}
        self.window = None
        self.window_title = window_title

    def __enter__(self):
        pygame.init()
        self.window = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(self.window_title)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def activate(self, engine):
        yield events.PreRender()
        yield events.Render()

    def on_render(self, render_event, signal):
        self.render_background(render_event.scene)
        camera = render_event.scene.main_camera
        camera.viewport_width, camera.viewport_height = self.resolution
        for game_object in render_event.scene:
            resource = self.prepare_resource(game_object)
            if resource is None:
                continue
            rectangle = self.prepare_rectangle(resource, game_object, camera)
            self.window.blit(resource, rectangle)
        pygame.display.update()

    def render_background(self, scene):
        self.window.fill(scene.background_color)

    def prepare_resource(self, game_object):
        image_name = game_object.__image__()
        if image_name is flags.DoNotRender:
            return None
        if image_name not in self.resources:
            self.register_renderable(game_object)
        # TODO: Rotate Image to facing.
        return self.resources[game_object.image]

    def prepare_rectangle(self, resource, game_object, camera):
        rect = resource.get_rect()
        rect.center = camera.translate_to_viewport(game_object.position)
        return rect

    def register(self, resource_path, name=None):
        try:
            resource = pygame.image.load(str(resource_path)).convert_alpha(self.window)
        except pygame.error:
            # Image didn't load, so either the name is bad or the file doesn't
            # exist. Instead, we'll render a square with a random color.
            resource = pygame.Surface((70, 70))
            random.seed(str(resource_path))
            r = random.randint(65, 255)
            g = random.randint(65, 255)
            b = random.randint(65, 255)
            resource.fill((r, g, b))
        name = name or resource_path
        self.resources[name] = resource

    def register_renderable(self, renderable):
        image_name = renderable.__image__()
        source_path = renderable.__resource_path__()
        self.register(source_path / image_name, image_name)


class Updater(System):

    def __init__(self, time_step=0.016, **kwargs):
        self.accumulated_time = 0
        self.last_tick = None
        self.start_time = None
        self.time_step = time_step

    def __enter__(self):
        self.start_time = time.time()

    def activate(self, engine):
        if self.last_tick is None:
            self.last_tick = time.time()
        this_tick = time.time()
        self.accumulated_time += this_tick - self.last_tick
        self.last_tick = this_tick
        while self.accumulated_time >= self.time_step:
            self.accumulated_time += -self.time_step
            yield events.Update(self.time_step)
