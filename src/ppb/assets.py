from ctypes import byref, c_int
from typing import NamedTuple, Tuple, Union

import sdl2.ext
from sdl2 import (
    SDL_Point,  # https://wiki.libsdl.org/SDL_Point
    SDL_CreateRGBSurface,  # https://wiki.libsdl.org/SDL_CreateRGBSurface
    SDL_FreeSurface,  # https://wiki.libsdl.org/SDL_FreeSurface
    SDL_SetColorKey,  # https://wiki.libsdl.org/SDL_SetColorKey
    SDL_CreateSoftwareRenderer,  # https://wiki.libsdl.org/SDL_CreateSoftwareRenderer
    SDL_DestroyRenderer,  # https://wiki.libsdl.org/SDL_DestroyRenderer
    SDL_SetRenderDrawColor,  # https://wiki.libsdl.org/SDL_SetRenderDrawColor
    SDL_RenderFillRect,  # https://wiki.libsdl.org/SDL_RenderFillRect
    SDL_GetRendererOutputSize,  # https://wiki.libsdl.org/SDL_GetRendererOutputSize
)

from sdl2.sdlgfx import (
    filledTrigonRGBA,  # https://www.ferzkopp.net/Software/SDL2_gfx/Docs/html/_s_d_l2__gfx_primitives_8h.html#a273cf4a88abf6c6a5e019b2c58ee2423
    filledCircleRGBA,  # https://www.ferzkopp.net/Software/SDL2_gfx/Docs/html/_s_d_l2__gfx_primitives_8h.html#a666bd764e2fe962656e5829d0aad5ba6
    filledEllipseRGBA,  # https://www.ferzkopp.net/Software/SDL2_gfx/Docs/html/_s_d_l2__gfx_primitives_8h.html#a5240918c243c3e60dd8ae1cef50dd529
)

from ppb.assetlib import BackgroundMixin, FreeingMixin, AbstractAsset
from ppb.systems.sdl_utils import sdl_call

__all__ = (
    "Rectangle",
    "Square",
    "Triangle",
    "Circle",
    "Ellipse"
)

BLACK = 0, 0, 0
MAGENTA = 255, 71, 182
DEFAULT_SPRITE_SIZE = 64


class AspectRatio(NamedTuple):
    width: Union[int, float]
    height: Union[int, float]


def _create_surface(color, aspect_ratio: AspectRatio = AspectRatio(1, 1)):
    """
    Creates a surface for assets and sets the color key.
    """
    width = height = DEFAULT_SPRITE_SIZE
    if aspect_ratio.width > aspect_ratio.height:
        height *= aspect_ratio.height / aspect_ratio.width
        height = int(height)
    elif aspect_ratio.height > aspect_ratio.width:
        width *= aspect_ratio.width / aspect_ratio.height
        width = int(width)

    surface = sdl_call(
        SDL_CreateRGBSurface, 0, width, height, 32, 0, 0, 0, 0,
        _check_error=lambda rv: not rv
    )
    color_key = BLACK if color != BLACK else MAGENTA
    color = sdl2.ext.Color(*color_key)
    sdl_call(
        SDL_SetColorKey, surface, True, sdl2.ext.prepare_color(color, surface.contents),
        _check_error=lambda rv: rv < 0
    )
    sdl2.ext.fill(surface.contents, color)
    return surface


aspect_ratio_type = Union[AspectRatio, Tuple[Union[float, int], Union[float, int]]]


class Shape(BackgroundMixin, FreeingMixin, AbstractAsset):
    """Shapes are drawing primitives that are good for rapid prototyping."""
    def __init__(self, red: int, green: int, blue: int, aspect_ratio: aspect_ratio_type = AspectRatio(1, 1)):
        self.color = red, green, blue
        self.aspect_ratio = AspectRatio(*aspect_ratio)
        self._start()

    def _background(self):
        surface = _create_surface(self.color, self.aspect_ratio)

        renderer = sdl_call(
            SDL_CreateSoftwareRenderer, surface,
            _check_error=lambda rv: not rv
        )
        try:
            self._draw_shape(renderer, rgb=self.color)
        finally:
            sdl_call(SDL_DestroyRenderer, renderer)
        return surface

    def free(self, surface, _SDL_FreeSurface=SDL_FreeSurface):
        SDL_FreeSurface(surface)

    def _draw_shape(self, renderer, **_) -> None:
        """
        Modify the raw asset to match the intended shape.
        """


class Rectangle(Shape):
    """
    A rectangle image of a single color.
    """

    def _draw_shape(self, renderer, rgb, **_):
        sdl_call(
            SDL_SetRenderDrawColor, renderer, *rgb, 255,
            _check_error=lambda rv: rv < 0
        )
        sdl_call(
            SDL_RenderFillRect, renderer, None,
            _check_error=lambda rv: rv < 0
        )


class Square(Rectangle):
    """
    A constructor for :class:`~ppb.Rectangle` that produces a square image.
    """

    def __init__(self, r, g, b):
        # This cuts out the aspect_ratio parameter
        super().__init__(r, g, b)


class Triangle(Shape):
    """
    A triangle image of a single color.
    """

    def _draw_shape(self, renderer, rgb, **_):
        w, h = c_int(), c_int()
        sdl_call(SDL_GetRendererOutputSize, renderer, byref(w), byref(h))
        width, height = w.value, h.value

        sdl_call(
            filledTrigonRGBA, renderer,
            0, height,
            int(width / 2), 0,
            width, height,
            *rgb, 255,
            _check_error=lambda rv: rv < 0
        )


class Ellipse(Shape):
    """
    An ellipse image of a single color.
    """

    def _draw_shape(self, renderer, rgb, **_):
        w, h = c_int(), c_int()
        sdl_call(SDL_GetRendererOutputSize, renderer, byref(w), byref(h))
        half_width, half_height = int(w.value / 2), int(h.value / 2)

        sdl_call(
            filledEllipseRGBA, renderer,
            half_width, half_height,  # Center
            half_width, half_height,  # Radius
            *rgb, 255,
            _check_error=lambda rv: rv < 0
        )


class Circle(Ellipse):
    """A convenience constructor for :class:`~ppb.Ellipse` that is a perfect circle."""

    def __init__(self, r, g, b):
        # This cuts out the aspect_ratio parameter
        super().__init__(r, g, b)
