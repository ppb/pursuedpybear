import ctypes
import io
import logging
import random
from time import monotonic

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
)

from sdl2.sdlimage import (
    IMG_GetError, IMG_SetError,  # https://www.libsdl.org/projects/SDL_image/docs/SDL_image_43.html#SEC43
    IMG_Load_RW,  # https://www.libsdl.org/projects/SDL_image/docs/SDL_image_12.html#SEC12
    IMG_Init, IMG_Quit,  # https://www.libsdl.org/projects/SDL_image/docs/SDL_image_6.html#SEC6
    IMG_INIT_JPG, IMG_INIT_PNG, IMG_INIT_TIF,
)

import ppb.assetlib as assets
import ppb.events as events
import ppb.flags as flags
from ppb.systems._sdl_utils import SdlSubSystem, sdl_call, SdlError
from ppb.systems._utils import ObjectSideData

logger = logging.getLogger(__name__)


DEFAULT_RESOLUTION = 800, 600


class ImgError(SdlError):
    pass


def img_call(func, *pargs, _check_error=None, **kwargs):
    """
    Wrapper for calling SDL functions for handling errors.

    If _check_error is given, called with the return value to check for errors.
    If _check_error returns truthy, an error occurred.

    If _check_error is not given, it is assumed that a non-empty error from
    Mix_GetError indicates error.
    """
    IMG_SetError(b"")
    rv = func(*pargs, **kwargs)
    err = IMG_GetError()
    if (_check_error(rv) if _check_error else err):
        raise SdlError(f"Error calling {func.__name__}: {err.decode('utf-8')}")
    else:
        return rv


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
        **kwargs
    ):
        self.resolution = resolution
        self.window = None
        self.window_title = window_title
        self.pixel_ratio = None
        self.target_frame_rate = target_frame_rate
        self.target_frame_length = 1 / self.target_frame_rate
        self.target_clock = monotonic() + self.target_frame_length

        self._texture_cache = ObjectSideData()

    def __enter__(self):
        super().__enter__()
        img_call(IMG_Init, IMG_INIT_JPG | IMG_INIT_PNG | IMG_INIT_TIF)
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
        img_call(IMG_Quit)
        super().__exit__(*exc)

    def on_idle(self, idle_event: events.Idle, signal):
        t = monotonic()
        if t >= self.target_clock:
            self.pre_render_updates(idle_event.scene)
            signal(events.PreRender())
            signal(events.Render())
            self.target_clock = t + self.target_frame_length

    def pre_render_updates(self, scene):
        camera = scene.main_camera
        camera.viewport_width, camera.viewport_height = self.resolution
        self.pixel_ratio = camera.pixel_ratio

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

    def prepare_resource(self, game_object):
        if game_object.size <= 0:
            return None

        image = game_object.__image__()
        if image is flags.DoNotRender or image is None:
            return None

        surface = image.load()
        try:
            return self._texture_cache[surface]
        except KeyError:
            texture = SmartPointer(sdl_call(
                SDL_CreateTextureFromSurface, self.renderer, surface,
                _check_error=lambda rv: not rv
            ), SDL_DestroyTexture)
            self._texture_cache[surface] = texture
            return texture

    def compute_rectangles(self, texture, game_object, camera):
        flags = sdl2.stdinc.Uint32()
        access = ctypes.c_int()
        img_w = ctypes.c_int()
        img_h = ctypes.c_int()
        sdl_call(
            SDL_QueryTexture, texture, ctypes.byref(flags), ctypes.byref(access),
            ctypes.byref(img_w), ctypes.byref(img_h),
            _check_error=lambda rv: rv < 0
        )

        src_rect = SDL_Rect(x=0, y=0, w=img_w, h=img_h)

        win_w, win_h = self.target_resolution(img_w.value, img_h.value, game_object.size)

        center = camera.translate_to_viewport(game_object.position)
        dest_rect = SDL_Rect(
            x=int(center.x - win_w / 2),
            y=int(center.y - win_h / 2),
            w=win_w,
            h=win_h,
        )

        return src_rect, dest_rect, ctypes.c_double(-game_object.rotation)

    def target_resolution(self, width, height, game_unit_size):
        values = [width, height]
        short_side_index = width > height
        target = self.pixel_ratio * game_unit_size
        ratio = values[short_side_index] / target
        return tuple(round(value / ratio) for value in values)
