import ctypes
from functools import lru_cache
import io
import logging
import random
from typing import Tuple

import sdl2
import sdl2.ext

from sdl2 import (
    rw_from_object,  # https://pysdl2.readthedocs.io/en/latest/modules/sdl2.html#sdl2.sdl2.rw_from_object
    SDL_Window, SDL_Renderer,
    SDL_Rect,  # https://wiki.libsdl.org/SDL_Rect
    SDL_INIT_VIDEO, SDL_BLENDMODE_BLEND, SDL_FLIP_NONE,
    SDL_CreateWindowAndRenderer,  # https://wiki.libsdl.org/SDL_CreateWindowAndRenderer
    SDL_DestroyRenderer,  # https://wiki.libsdl.org/SDL_DestroyRenderer
    SDL_DestroyWindow,  # https://wiki.libsdl.org/SDL_DestroyWindow
    SDL_SetWindowTitle,  # https://wiki.libsdl.org/SDL_SetWindowTitle
    SDL_RenderPresent,  # https://wiki.libsdl.org/SDL_RenderPresent
    SDL_RenderClear,  # https://wiki.libsdl.org/SDL_RenderClear
    SDL_SetRenderDrawColor,  # https://wiki.libsdl.org/SDL_SetRenderDrawColor
    SDL_FreeSurface,  # https://wiki.libsdl.org/SDL_FreeSurface
    SDL_SetSurfaceBlendMode,  # https://wiki.libsdl.org/SDL_SetSurfaceBlendMode
    SDL_CreateTextureFromSurface,  # https://wiki.libsdl.org/SDL_CreateTextureFromSurface
    SDL_DestroyTexture,  # https://wiki.libsdl.org/SDL_DestroyTexture
    SDL_QueryTexture,  # https://wiki.libsdl.org/SDL_QueryTexture
    SDL_RenderCopyEx,  # https://wiki.libsdl.org/SDL_RenderCopyEx
    SDL_CreateRGBSurface,  # https://wiki.libsdl.org/SDL_CreateRGBSurface
    SDL_BLENDMODE_ADD,
    SDL_BLENDMODE_BLEND,
    SDL_BLENDMODE_MOD,
    SDL_BLENDMODE_NONE,
    SDL_SetTextureAlphaMod,
    SDL_SetTextureBlendMode,
    SDL_SetTextureColorMod,
)

from sdl2.sdlimage import (
    IMG_Load_RW,  # https://www.libsdl.org/projects/SDL_image/docs/SDL_image_12.html#SEC12
    IMG_Init, IMG_Quit,  # https://www.libsdl.org/projects/SDL_image/docs/SDL_image_6.html#SEC6
    IMG_INIT_JPG, IMG_INIT_PNG, IMG_INIT_TIF,
)

from sdl2.sdlttf import (
    TTF_Init, TTF_Quit,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_6.html#SEC6
)


import ppb.assetlib as assets
import ppb.events as events
import ppb.flags as flags

from ppb.camera import Camera
from ppb.systems._sdl_utils import SdlSubSystem, sdl_call, img_call, ttf_call
from ppb.systems._utils import ObjectSideData
from ppb.utils import get_time

logger = logging.getLogger(__name__)


DEFAULT_RESOLUTION = 800, 600

OPACITY_MODES = {
    flags.BlendModeAdd: SDL_BLENDMODE_ADD,
    flags.BlendModeBlend: SDL_BLENDMODE_BLEND,
    flags.BlendModeMod: SDL_BLENDMODE_MOD,
    flags.BlendModeNone: SDL_BLENDMODE_NONE,
}


# TODO: Move Image out of the renderer so sprites can type hint appropriately.
class Image(assets.Asset):
    # Wraps POINTER(SDL_Surface)

    def background_parse(self, data):
        file = rw_from_object(io.BytesIO(data))
        # ^^^^ is a pure-python emulation, does not need cleanup.
        surface = img_call(
            IMG_Load_RW, file, False,
            _check_error=lambda rv: not rv
        )

        sdl_call(
            SDL_SetSurfaceBlendMode, surface, SDL_BLENDMODE_BLEND,
            _check_error=lambda rv: rv < 0
        )

        return surface

    def file_missing(self):
        width = height = 70  # Pixels, arbitrary
        surface = sdl_call(
            SDL_CreateRGBSurface, 0, width, height, 32, 0, 0, 0, 0,
            _check_error=lambda rv: not rv
        )

        rand = random.Random(str(self.name))
        r = rand.randint(65, 255)
        g = rand.randint(65, 255)
        b = rand.randint(65, 255)
        color = sdl2.ext.Color(r, g, b)

        sdl2.ext.fill(surface.contents, color)
        return surface

    def free(self, object, _SDL_FreeSurface=SDL_FreeSurface):
        # ^^^ is a way to keep required functions during interpreter cleanup

        _SDL_FreeSurface(object)  # Can't fail
        # object.contents = None
        # Can't actually nullify the pointer. Good thing this is __del__.


class SmartPointer:
    def __init__(self, obj, dest):
        self.inner = obj
        self.destructor = dest

    def __del__(self):
        self.destructor(self.inner)


class Renderer(SdlSubSystem):
    _sdl_subsystems = SDL_INIT_VIDEO

    def __init__(
        self,
        resolution=DEFAULT_RESOLUTION,
        window_title: str = "PursuedPyBear",
        target_frame_rate: int = 30,
        target_camera_width=25,
        **kwargs
    ):
        self.resolution = resolution
        self.window = None
        self.window_title = window_title
        self.scene_cameras = {}
        self.target_camera_width = target_camera_width
        self.target_frame_rate = target_frame_rate
        self.target_frame_length = 1 / self.target_frame_rate
        self.target_clock = get_time() + self.target_frame_length
        self.last_opacity = 255
        self.last_opacity_mode = OPACITY_MODES[flags.BlendModeNone]
        self.last_tint = (255, 255, 255)

        self._texture_cache = ObjectSideData()

    def __enter__(self):
        super().__enter__()
        img_call(IMG_Init, IMG_INIT_JPG | IMG_INIT_PNG | IMG_INIT_TIF)
        ttf_call(TTF_Init, _check_error=lambda rv: rv == -1)
        self.window = ctypes.POINTER(SDL_Window)()
        self.renderer = ctypes.POINTER(SDL_Renderer)()
        sdl_call(
            SDL_CreateWindowAndRenderer,
            self.resolution[0],  # Width
            self.resolution[1],  # Height
            0,  # Flags
            # SDL_WINDOW_ALLOW_HIGHDPI - Allow the renderer to work in HiDPI natively
            ctypes.byref(self.window),
            ctypes.byref(self.renderer),
            _check_error=lambda rv: rv < 0
        )
        # NOTE: It looks like SDL_RENDERER_PRESENTVSYNC will cause SDL_RenderPresent() to block?
        sdl_call(SDL_SetWindowTitle, self.window, self.window_title.encode('utf-8'))

    def __exit__(self, *exc):
        sdl_call(SDL_DestroyRenderer, self.renderer)
        sdl_call(SDL_DestroyWindow, self.window)
        ttf_call(TTF_Quit)
        img_call(IMG_Quit)
        super().__exit__(*exc)

    def on_idle(self, idle_event: events.Idle, signal):
        t = get_time()
        if t >= self.target_clock:
            signal(events.PreRender())
            signal(events.Render())
            self.target_clock = t + self.target_frame_length

    def on_scene_started(self, scene_started, signal):
        scene = scene_started.scene
        camera_class = getattr(scene_started.scene, "camera_class", Camera)
        # For future: This is basically the pattern we'd use to define
        # multiple cameras. We'd just need to have the scene tell us the
        # regions they should render to.
        camera = camera_class(self, self.target_camera_width, self.resolution)
        scene.main_camera = camera
        self.scene_cameras[scene] = [camera]

    def on_scene_stopped(self, scene_stopped, signal):
        """We don't need to hold onto references for scenes that stopped."""
        del self.scene_cameras[scene_stopped.scene]

    def on_render(self, render_event, signal):
        camera = render_event.scene.main_camera

        self.render_background(render_event.scene)

        for game_object in render_event.scene.sprite_layers():
            texture = self.prepare_resource(game_object)
            if texture is None:
                continue
            src_rect, dest_rect, angle = self.compute_rectangles(
                texture.inner, game_object, camera
            )
            sdl_call(
                SDL_RenderCopyEx, self.renderer, texture.inner,
                ctypes.byref(src_rect), ctypes.byref(dest_rect),
                angle, None, SDL_FLIP_NONE,
                _check_error=lambda rv: rv < 0
            )
        sdl_call(SDL_RenderPresent, self.renderer)

    def render_background(self, scene):
        bg = scene.background_color
        sdl_call(
            SDL_SetRenderDrawColor, self.renderer, bg[0], bg[1], bg[2], 255,
            _check_error=lambda rv: rv < 0
        )
        sdl_call(SDL_RenderClear, self.renderer, _check_error=lambda rv: rv < 0)

    def _object_has_dimension(self, game_object):
        """
        Tests that an object has dimensionality and they're >0.
        """
        if hasattr(game_object, 'width') and game_object.width <= 0:
            return False
        elif hasattr(game_object, 'height') and game_object.height <= 0:
            return False
        elif hasattr(game_object, 'size') and game_object.size <= 0:
            return False
        elif not (hasattr(game_object, 'width') or hasattr(game_object, 'height') or hasattr(game_object, 'size')):
            return False
        else:
            return True

    def prepare_resource(self, game_object):
        """
        Get the SDL Texture for an object.
        """
        if not self._object_has_dimension(game_object):
            return None

        if not hasattr(game_object, '__image__'):
            return None

        try:
            image = game_object.__image__()
        except AttributeError:
            return None
        else:
            if image is flags.DoNotRender or image is None:
                return None

        # Can change for animated objects, cannot reliable cache
        surface = image.load()
        try:
            texture = self._texture_cache[surface]
        except KeyError:
            texture = SmartPointer(sdl_call(
                SDL_CreateTextureFromSurface, self.renderer, surface,
                _check_error=lambda rv: not rv
            ), SDL_DestroyTexture)
            self._texture_cache[surface] = texture

        opacity = getattr(game_object, 'opacity', 255)
        opacity_mode = getattr(game_object, 'opacity_mode', flags.BlendModeBlend)
        opacity_mode = OPACITY_MODES[opacity_mode]
        tint = getattr(game_object, 'tint', (255, 255, 255))

        if self.last_opacity != opacity:
            self.last_opacity = opacity
            sdl_call(
                SDL_SetTextureAlphaMod, texture.inner, opacity,
                _check_error=lambda rv: rv < 0
            )

        if self.last_opacity_mode != opacity_mode:
            self.last_opacity_mode = opacity_mode
            sdl_call(
                SDL_SetTextureBlendMode, texture.inner, opacity_mode,
                _check_error=lambda rv: rv < 0
            )

        if self.last_tint != tint:
            self.last_tine = tint
            sdl_call(
                SDL_SetTextureColorMod, texture.inner, tint[0], tint[1], tint[2],
                _check_error=lambda rv: rv < 0
            )

        return texture

    _compute_cache = {}
    def compute_rectangles(self, texture, game_object, camera):
        if hasattr(game_object, 'width'):
            obj_w = game_object.width
            obj_h = game_object.height
        else:
            obj_w, obj_h = game_object.size

        rect = getattr(game_object, 'rect', None)
        key = (rect, id(texture), tuple(game_object.position), obj_w, obj_h, camera.pixel_ratio,)

        try:
            win_w, win_h, src_rect, dest_rect = self._compute_cache[key]
        except KeyError:    
            self._compute_cache[key] = self._compute_rectangles(
                rect,
                texture,
                game_object.position,
                obj_w, obj_h, camera.pixel_ratio,
                camera,
            )
            win_w, win_h, src_rect, dest_rect = self._compute_cache[key]

        return src_rect, dest_rect, ctypes.c_double(-game_object.rotation)
    
    @staticmethod
    def _compute_rectangles(rect, texture, position, obj_width, obj_height, pixel_ratio, camera):
        flags = sdl2.stdinc.Uint32()
        access = ctypes.c_int()
        img_w = ctypes.c_int()
        img_h = ctypes.c_int()
        sdl_call(
            SDL_QueryTexture, texture, ctypes.byref(flags), ctypes.byref(access),
            ctypes.byref(img_w), ctypes.byref(img_h),
            _check_error=lambda rv: rv < 0
        )

        if rect:
            src_rect = SDL_Rect(*rect)
            win_w = int(rect[2] * obj_width)
            win_h = int(rect[3] * obj_height)
        else:
            src_rect = SDL_Rect(x=0, y=0, w=img_w, h=img_h)

            if not obj_width:
                print("no width")
                ratio = img_h / (pixel_ratio * obj_height)
            elif not obj_height:
                print("no height")
                ratio = img_w.value / (pixel_ratio * obj_width)
            else:
                ratio_w = img_w.value / (pixel_ratio * obj_width)
                ratio_h = img_h.value / (pixel_ratio * obj_height)
                ratio = min(ratio_w, ratio_h)  # smaller value -> less reduction
            
            win_w, win_h = round(img_w.value / ratio), round(img_h.value / ratio)

        center = camera.translate_point_to_screen(position)
        dest_rect = SDL_Rect(
            x=int(center.x - win_w / 2),
            y=int(center.y - win_h / 2),
            w=win_w,
            h=win_h,
        )

        return win_w, win_h, src_rect, dest_rect
