import random
import time

import pygame

import ppb.events as events
import ppb.flags as flags

default_resolution = 800, 600


class System(events.EventMixin):

    def __init__(self, **_):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


from ppb.systems.pg import EventPoller as PygameEventPoller  # To not break old imports.


class Renderer(System):

    def __init__(self, resolution=default_resolution, window_title: str="PursuedPyBear", target_frame_rate: int=30, **kwargs):
        self.resolution = resolution
        self.resources = {}
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

        for game_object in render_event.scene:
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
        image_name = game_object.__image__()
        if image_name is flags.DoNotRender:
            return None
        image_name = str(image_name)
        if image_name not in self.resources:
            self.register_renderable(game_object)

        source_image = self.resources[image_name]
        if game_object.size <= 0:
            return None
        resized_image = self.resize_image(source_image, game_object.size)
        rotated_image = self.rotate_image(resized_image, game_object.rotation)
        return rotated_image

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
        image_name = str(renderable.__image__())
        source_path = renderable.__resource_path__()
        self.register(source_path / image_name, image_name)

    def resize_image(self, image, game_unit_size):
        # TODO: Pygame specific code To be abstracted somehow.
        key = (image, game_unit_size)
        resized_image = self.old_resized_images.get(key)
        if  resized_image is None:
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


class Updater(System):

    def __init__(self, time_step=0.016, **kwargs):
        self.accumulated_time = 0
        self.last_tick = None
        self.start_time = None
        self.time_step = time_step

    def __enter__(self):
        self.start_time = time.monotonic()

    def on_idle(self, idle_event: events.Idle, signal):
        if self.last_tick is None:
            self.last_tick = time.monotonic()
        this_tick = time.monotonic()
        self.accumulated_time += this_tick - self.last_tick
        self.last_tick = this_tick
        while self.accumulated_time >= self.time_step:
            # This might need to change for the Idle event system to signal _only_ once per idle event.
            self.accumulated_time += -self.time_step
            signal(events.Update(self.time_step))
