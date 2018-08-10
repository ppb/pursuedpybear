import pygame

from ppb import Vector
from ppb.events import EventMixin

class System(EventMixin):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def activate(self, engine):
        return []


class Renderer:

    def __init__(self):
        self.resources = {}
        self.window = None
        self.offset = None
        self.camera_position = Vector(0, 0)

    def render(self, scene):
        self.render_background(scene)
        for game_object in scene:
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

    def start(self):
        self.window = pygame.display.get_surface()
        self.offset = Vector(-0.5 * self.window.get_width(),
                             -0.5 * self.window.get_height())
