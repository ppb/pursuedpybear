import pygame

from ppb import Vector
from ppb.events import EventMixin
from ppb.events import Prerender
from ppb.events import Quit
from ppb.events import Render


class System(EventMixin):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def activate(self, engine):
        return []



class Quitter(System):
    """
    System for running test. Limits the engine to a single loop.
    """

    def activate(self, engine):
        yield Quit()


class Renderer(System):

    def __init__(self):
        self.resolution = 600, 400
        self.resources = {}
        self.window = None
        self.offset = None
        self.camera_position = Vector(0, 0)

    def __enter__(self):
        pygame.init()
        self.window = pygame.display.set_mode(self.resolution)
        self.offset = Vector(-0.5 * self.window.get_width(),
                             -0.5 * self.window.get_height())

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def activate(self, engine):
        yield Prerender()
        yield Render()

    def on_render(self, render_event, signal):
        self.render_background(render_event.scene)
        for game_object in render_event.scene:
            resource = self.prepare_resource(game_object)
            rectangle = self.prepare_rectangle(resource, game_object)
            self.window.blit(resource, rectangle)
        pygame.display.update()

    def render_background(self, scene):
        self.window.fill(scene.background_color)

    def prepare_resource(self, game_object):
        image_name = game_object.__image__()
        if image_name not in self.resources:
            self.register_renderable(game_object)
        # TODO: Rotate Image to facing.
        return self.resources[game_object.image]

    def prepare_rectangle(self, resource, game_object):
        rect = resource.get_rect()
        rect.center = game_object.position - (self.offset - self.camera_position)
        return rect

    def register(self, resource_path, name=None):
        resource = pygame.image.load(str(resource_path)).convert_alpha(self.window)
        name = name or resource_path
        self.resources[name] = resource

    def register_renderable(self, renderable):
        image_name = renderable.__image__()
        source_path = renderable.__resource_path__()
        self.register(source_path / image_name, image_name)
