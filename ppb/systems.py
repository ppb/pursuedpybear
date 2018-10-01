import random
import time
from typing import Union
from typing import Iterable
import functools

import pyglet

import ppb.events as events
import ppb.flags as flags
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


class Quitter(System):
    """
    System for running test. Limits the engine to a single loop.
    """

    def activate(self, engine):
        yield events.Quit()


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

    def _insert_call(self, obj, attr, call):
        old_call = getattr(obj, attr)
        @functools.wraps(old_call)
        def _wrap(*p, **kw):
            call(obj, *p, **kw)
            return old_call(*p, **kw)
        setattr(obj, attr, _wrap)

    ### DRAWING ###

    def _update_camera(self, scene):
        camera = scene.main_camera
        camera.viewport_width = self.window.width
        camera.viewport_height = self.window.height

    def on_resize(self, width, height):
        scene = self.engine.current_scene
        if scene is not None:
            self._update_camera(scene)

    def _load_resource(self, img):
        res = pyglet.resource.image(img)
        res.anchor_x = res.width / 2
        res.anchor_y = res.height / 2
        return res

    def _scene_add_sprite(self, scene, sprite, tags=()):
        img = sprite.__image__()
        sprite.__prev_image = img
        if img is flags.DoNotRender:
            sprite.__resource = None
            sprite.__sprite = None
        else:
            # FIXME: The resource path is relative to the source file, use __resource_path__()
            sprite.__resource = self._load_resource(img)
            pos = scene.main_camera.translate_to_viewport(sprite.position)
            sprite.__sprite = pyglet.sprite.Sprite(
                img=sprite.__resource,
                x=pos.x,
                y=pos.y,
                batch=scene.__batch,
            )

    def _update_sprite(self, scene, sprite):
        img = sprite.__image__()
        if img is flags.DoNotRender and sprite.__prev_image is not flags.DoNotRender:
            # The sprite has been hidden, delete its resources
            s = sprite.__sprite
            s.batch = None
            s.delete()
            sprite.__resource = None
            sprite.__sprite = None
        elif img is not flags.DoNotRender:
            # Sprite is visible, update
            if img != sprite.__prev_image:
                sprite.__resource = self._load_resource(img)
                sprite.__prev_image = img
                sprite.__sprite.image = sprite.__resource
            pos = scene.main_camera.translate_to_viewport(sprite.position)
            sprite.__sprite.update(
                x=pos.x,
                y=pos.y,
            )

    def _scene_remove_sprite(self, scene, sprite):
        sprite.__sprite.batch = None
        sprite.__sprite.delete()
        sprite.__sprite = None
        sprite.__resource = None
        sprite.__prev_image = None

    def _annotate_scene(self, scene):
        scene.__batch = batch = pyglet.graphics.Batch()
        self._insert_call(scene, 'add', self._scene_add_sprite)
        self._insert_call(scene, 'remove', self._scene_remove_sprite)
        for sprite in scene:
            self._scene_add_sprite(scene, sprite)

    def _scan_scene(self, scene):
        for sprite in scene:
            if sprite._dirty:
                self._update_sprite(scene, sprite)
            sprite.__dict__['_dirty'] = False

    def on_draw(self):
        self.engine.signal(events.PreRender())
        scene = self.engine.current_scene
        try:
            scene.__batch
        except AttributeError:
            self._annotate_scene(scene)

        self._update_camera(scene)
        self._scan_scene(scene)

        self.window.clear()
        scene.__batch.draw()

    ### MOUSE HANDLING ###

    def on_mouse_motion(self, x, y, dx, dy):
        cam = self.engine.current_scene.main_camera
        p = cam.translate_to_frame(Vector(x, y))
        d = cam.translate_to_frame(Vector(dx, dy))
        self.engine.signal(events.MouseMotion(
            position=p,
            delta=d,
            buttons=[False] * 3,
        ))

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        cam = self.engine.current_scene.main_camera
        buttons = [
            buttons & 0b1,
            buttons & 0b100,
            buttons & 0b10,
        ]
        p = cam.translate_to_frame(Vector(x, y))
        d = cam.translate_to_frame(Vector(dx, dy))
        self.engine.signal(events.MouseMotion(
            position=p,
            delta=d,
            buttons=buttons,
        ))
