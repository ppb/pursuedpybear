import random
import time
from typing import Union
from typing import Iterable

import pyglet

import ppb.events as events
import ppb.flags as flags
from ppb.mouse import Mouse
from ppb.vector import Vector

default_resolution = 800, 600


class System(events.EventMixin):

    def __init__(self, *, engine, **_):
        self.engine = engine  # XXX: Does this need to be a weakref?

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def activate(self, engine):
        return []


# class PygameEventPoller(System):
#     """
#     An event poller that converts Pygame events into PPB events.
#     """

#     event_map = None

#     def __new__(cls, *args, **kwargs):
#         if cls.event_map is None:
#             cls.event_map = {
#                 pygame.QUIT: "quit",
#                 pygame.MOUSEMOTION: "mouse_motion",
#             }
#         return super().__new__(cls)

#     def __init__(self, resolution=default_resolution, **kwargs):
#         self.offset = Vector(-0.5 * resolution[0],
#                              -0.5 * resolution[1])

#     def __enter__(self):
#         pygame.init()

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pygame.quit()

#     def on_update(self, update, signal):
#         for pygame_event in pygame.event.get():
#             ppb_event = self.event_map.get(pygame_event.type)
#             if ppb_event is not None:
#                 signal(getattr(self, ppb_event)(pygame_event, update.scene))

#     def quit(self, event, scene):
#         return events.Quit()

#     def mouse_motion(self, event, scene):
#         screen_position = Vector(*event.pos)
#         camera = scene.main_camera
#         game_position = camera.translate_to_frame(screen_position)
#         delta = Vector(*event.rel) * (1/camera.pixel_ratio)
#         buttons = [bool(x) for x in event.buttons]
#         return events.MouseMotion(game_position, screen_position, delta, buttons)

# class MouseSystem(System):
#     """
#     Mouse system.
#     """

#     def __init__(self, *, engine, resolution=default_resolution, **kwargs):
#         self.mouse = Mouse()
#         self.offset = Vector(-0.5 * resolution[0],
#                              -0.5 * resolution[1])
#         engine.register(events.Update, "mouse", self.mouse)

#     def activate(self, engine):
#         """Sync mouse with hardware."""
#         buttons = self.get_hardware_buttons()
#         if buttons is not None:
#             self.mouse.buttons = [bool(x) for x in buttons]
#         screen_position = self.get_hardware_position()
#         if screen_position is not None:
#             camera = engine.current_scene.main_camera
#             self.mouse.screen_position = Vector(*screen_position)
#             self.mouse.position = camera.translate_to_frame(self.mouse.screen_position)
#         return []

#     def on_mouse_motion(self, mouse_motion_event, signal):
#         self.mouse.buttons = mouse_motion_event.buttons
#         self.mouse.screen_position = mouse_motion_event.screen_position
#         self.mouse.position = mouse_motion_event.position

#     def get_hardware_buttons(self) -> Union[Iterable, None]:
#         pass

#     def get_hardware_position(self) -> Union[Iterable, None]:
#         pass


# class PygameMouseSystem(MouseSystem):

#     def get_hardware_buttons(self):
#         return pygame.mouse.get_pressed()

#     def get_hardware_position(self):
#         return pygame.mouse.get_pos()


class Quitter(System):
    """
    System for running test. Limits the engine to a single loop.
    """

    def activate(self, engine):
        yield events.Quit()


# class Renderer(System):

#     def __init__(self, resolution=default_resolution, **kwargs):
#         self.resolution = resolution
#         self.resources = {}
#         self.window = None

#     def __enter__(self):
#         pygame.init()
#         self.window = pygame.display.set_mode(self.resolution)

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pygame.quit()

#     def activate(self, engine):
#         yield events.PreRender()
#         yield events.Render()

#     def on_render(self, render_event, signal):
#         self.render_background(render_event.scene)
#         camera = render_event.scene.main_camera
#         camera.viewport_width, camera.viewport_height = self.resolution
#         for game_object in render_event.scene:
#             resource = self.prepare_resource(game_object)
#             if resource is None:
#                 continue
#             rectangle = self.prepare_rectangle(resource, game_object, camera)
#             self.window.blit(resource, rectangle)
#         pygame.display.update()

#     def render_background(self, scene):
#         self.window.fill(scene.background_color)

#     def prepare_resource(self, game_object):
#         image_name = game_object.__image__()
#         if image_name is flags.DoNotRender:
#             return None
#         if image_name not in self.resources:
#             self.register_renderable(game_object)
#         # TODO: Rotate Image to facing.
#         return self.resources[game_object.image]

#     def prepare_rectangle(self, resource, game_object, camera):
#         rect = resource.get_rect()
#         rect.center = camera.translate_to_viewport(game_object.position)
#         return rect

#     def register(self, resource_path, name=None):
#         try:
#             resource = pygame.image.load(str(resource_path)).convert_alpha(self.window)
#         except pygame.error:
#             # Image didn't load, so either the name is bad or the file doesn't
#             # exist. Instead, we'll render a square with a random color.
#             resource = pygame.Surface((70, 70))
#             random.seed(str(resource_path))
#             r = random.randint(65, 255)
#             g = random.randint(65, 255)
#             b = random.randint(65, 255)
#             resource.fill((r, g, b))
#         name = name or resource_path
#         self.resources[name] = resource

#     def register_renderable(self, renderable):
#         image_name = renderable.__image__()
#         source_path = renderable.__resource_path__()
#         self.register(source_path / image_name, image_name)


class Updater(System):
    def __init__(self, *, time_step=1 / 60, **kwargs):
        super().__init__(**kwargs)
        
        self.time_step = time_step

    def __enter__(self):
        pyglet.clock.schedule_interval(self._tick, self.time_step)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pyglet.clock.unschedule(self._tick)

    def _tick(self, dt):
        self.engine.signal(events.Update(time_delta=dt))


class PygletWindow(System):
    def __init__(self, *, window_title=None, resolution=default_resolution, **kw):
        super().__init__(**kw)
        self.window = pyglet.window.Window(
            visible=False,
            resizable=False,
            caption=window_title,
            width=resolution[0],
            height=resolution[1],
        )

        self._mouse_buttons = [False, False, False]

        # Dynamic pyglet event registration
        for attr in self.window.event_types:
            if hasattr(self, attr):
                self.window.event(getattr(self, attr))

    def __enter__(self):
        self.window.set_visible(True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.window.set_visible(False)

    def __event__(self, event, signal):
        # We're handling event dispatch ourselves, so that we don't have
        # conflicts with pyglet.
        meth_name = 'on_ppb_' + type(event).__name__
        meth = getattr(self, meth_name, None)
        if meth is not None:
            meth(event, signal)

    def on_mouse_motion(self, x, y, dx, dy):
        self.engine.signal(events.MouseMotion(
            position=Vector(x, y),
            delta=Vector(dx, dy),
            buttons=[False] * 3,
        ))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        buttons = [
            buttons & 0b1,
            buttons & 0b100,
            buttons & 0b10,
        ]
        self.engine.signal(events.MouseMotion(
            position=Vector(x, y),
            delta=Vector(dx, dy),
            buttons=[False] * 3,
        ))
