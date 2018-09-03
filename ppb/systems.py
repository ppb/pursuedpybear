import random
import time

import pygame

import ppb.events as events
import ppb.flags as flags

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

    event_map = {
        pygame.QUIT: events.Quit,
    }

    def __enter__(self):
        pygame.init()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def on_update(self, update, signal):
        for pygame_event in pygame.event.get():
            ppb_event = self.event_map.get(pygame_event.type)
            if ppb_event is not None:
                signal(ppb_event())


class Quitter(System):
    """
    System for running test. Limits the engine to a single loop.
    """

    def activate(self, engine):
        yield events.Quit()


class Renderer(System):

    def __init__(self, resolution=(800, 600), **kwargs):
        self.resolution = resolution
        self.resources = {}
        self.window = None

    def __enter__(self):
        pygame.init()
        self.window = pygame.display.set_mode(self.resolution)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def activate(self, engine):
        yield events.PreRender()
        yield events.Render()

    def on_render(self, render_event, signal):
        self.render_background(render_event.scene)
        camera = list(render_event.scene.get(tag="main_camera"))[0]
        camera.viewport_height, camera.viewport_width = self.resolution
        for game_object in render_event.scene:
            resource = self.prepare_resource(game_object)
            if resource is None:
                continue
            rectangle = self.prepare_rectangle(resource, game_object, camera)
            self.window.blit(resource, rectangle)
        pygame.display.update()
        pygame.event.pump()

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
            random.seed(hash(resource_path))
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
