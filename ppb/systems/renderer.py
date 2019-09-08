import io
import logging
import random

import pygame

import ppb.assetlib as assets
import ppb.events as events
import ppb.flags as flags
from ppb.systemslib import System

logger = logging.getLogger(__name__)


DEFAULT_RESOLUTION = 800, 600


# TODO: Move Image out of the renderer so sprites can type hint
#  appropriately.
class Image(assets.Asset):
    def background_parse(self, data):
        return pygame.image.load(io.BytesIO(data), self.name).convert_alpha()

    def file_missing(self):
        resource = pygame.Surface((70, 70))
        # this algorithm can't produce black, so this is a safe colorkey.
        resource.set_colorkey((0, 0, 0))
        random.seed(str(self.name))
        r = random.randint(65, 255)
        g = random.randint(65, 255)
        b = random.randint(65, 255)
        resource.fill((r, g, b))
        return resource


class Renderer(System):

    def __init__(
        self,
        resolution=DEFAULT_RESOLUTION,
        window_title: str = "PursuedPyBear",
        target_frame_rate: int = 30,
        **kwargs
    ):
        self.resolution = resolution
        self.window = None
        self.window_title = window_title
        self.pixel_ratio = None
        self.resized_images = {}
        self.old_resized_images = {}
        self.render_clock = 0
        self.target_frame_rate = target_frame_rate
        self.target_count = 1 / self.target_frame_rate

    def __enter__(self):
        pygame.init()
        self.window = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(self.window_title)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def on_idle(self, idle_event: events.Idle, signal):
        self.render_clock += idle_event.time_delta
        if self.render_clock > self.target_count:
            self.pre_render_updates(idle_event.scene)
            signal(events.PreRender())
            signal(events.Render())
            self.render_clock = 0

    def on_render(self, render_event, signal):
        camera = render_event.scene.main_camera
        self.render_background(render_event.scene)

        self.old_resized_images = self.resized_images
        self.resized_images = {}

        for game_object in render_event.scene.sprite_layers():
            resource = self.prepare_resource(game_object)
            if resource is None:
                continue
            rectangle = self.prepare_rectangle(resource, game_object, camera)
            self.window.blit(resource, rectangle)
        pygame.display.update()

    def pre_render_updates(self, scene):
        camera = scene.main_camera
        camera.viewport_width, camera.viewport_height = self.resolution
        self.pixel_ratio = camera.pixel_ratio

    def render_background(self, scene):
        self.window.fill(scene.background_color)

    def prepare_resource(self, game_object):
        image = game_object.__image__()
        if image is flags.DoNotRender:
            return None
        if isinstance(image, str):
            logger.warning(f"Using string resources is deprecated, use ppb.Image instead. Got {image!r}")
            image = Image(image)

        source_image = image.load()
        if game_object.size <= 0:
            return None
        resized_image = self.resize_image(source_image, game_object.size)
        rotated_image = self.rotate_image(resized_image, game_object.rotation)
        return rotated_image

    def prepare_rectangle(self, resource, game_object, camera):
        rect = resource.get_rect()
        rect.center = camera.translate_to_viewport(game_object.position)
        return rect

    def resize_image(self, image, game_unit_size):
        # TODO: Pygame specific code To be abstracted somehow.
        key = (image, game_unit_size)
        resized_image = self.old_resized_images.get(key)
        if resized_image is None:
            height = image.get_height()
            width = image.get_width()
            target_resolution = self.target_resolution(width,
                                                       height,
                                                       game_unit_size)
            resized_image = pygame.transform.smoothscale(image,
                                                         target_resolution)
        self.resized_images[key] = resized_image
        return resized_image

    def rotate_image(self, image, rotation):
        """Rotates image clockwise {rotation} degrees."""
        return pygame.transform.rotate(image, rotation)

    def target_resolution(self, width, height, game_unit_size):
        values = [width, height]
        short_side_index = width > height
        target = self.pixel_ratio * game_unit_size
        ratio = values[short_side_index] / target
        return tuple(round(value / ratio) for value in values)
