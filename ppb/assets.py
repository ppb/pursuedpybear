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
)

from sdl2.sdlgfx import (
    filledTrigonRGBA,  # https://www.ferzkopp.net/Software/SDL2_gfx/Docs/html/_s_d_l2__gfx_primitives_8h.html#a273cf4a88abf6c6a5e019b2c58ee2423
    filledCircleRGBA,  # https://www.ferzkopp.net/Software/SDL2_gfx/Docs/html/_s_d_l2__gfx_primitives_8h.html#a666bd764e2fe962656e5829d0aad5ba6
)

from ppb.assetlib import AbstractAsset
from ppb.systems._sdl_utils import sdl_call

__all__ = (
    "Square",
    "Triangle",
    "Circle",
)

BLACK = 0, 0, 0
MAGENTA = 255, 71, 182
DEFAULT_SPRITE_SIZE = 64


def _create_surface(color):
    """
    Creates a surface for assets and sets the color key.
    """
    surface = sdl_call(
        SDL_CreateRGBSurface, 0, DEFAULT_SPRITE_SIZE, DEFAULT_SPRITE_SIZE, 32, 0, 0, 0, 0,
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


class Shape(AbstractAsset):
    """Shapes are drawing primitives that are good for rapid prototyping."""
    _surface = None
    def __init__(self, red: int, green: int, blue: int):
        color = red, green, blue
        self._surface = _create_surface(color)

        renderer = sdl_call(
            SDL_CreateSoftwareRenderer, self._surface,
            _check_error=lambda rv: not rv
        )
        try:
            self._draw_shape(renderer, rgb=color)
        finally:
            sdl_call(SDL_DestroyRenderer, renderer)

    def load(self):
        """Return the underlying asset."""
        return self._surface

    def __del__(self, _SDL_FreeSurface=SDL_FreeSurface):
        if self._surface:
            SDL_FreeSurface(self._surface)

    def _draw_shape(self, renderer, **_) -> None:
        """
        Modify the raw asset to match the intended shape.
        """


class Square(Shape):
    """
    A square image of a single color.
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


class Triangle(Shape):
    """
    A triangle image of a single color.
    """

    def _draw_shape(self, renderer, rgb, **_):
        sdl_call(
            filledTrigonRGBA, renderer,
            0, DEFAULT_SPRITE_SIZE,
            int(DEFAULT_SPRITE_SIZE / 2), 0,
            DEFAULT_SPRITE_SIZE, DEFAULT_SPRITE_SIZE,
            *rgb, 255,
            _check_error=lambda rv: rv < 0
        )


class Circle(Shape):
    """
    A circle image of a single color.
    """

    def _draw_shape(self, renderer, rgb, **_):
        half = int(DEFAULT_SPRITE_SIZE / 2)
        sdl_call(
            filledCircleRGBA, renderer,
            half, half,  # Center
            half,  # Radius
            *rgb, 255,
            _check_error=lambda rv: rv < 0
        )
