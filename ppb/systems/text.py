import io

from sdl2 import rw_from_object

from sdl2.sdlttf import (
    TTF_OpenFontRW,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_15.html
    TTF_OpenFontIndexRW,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_17.html
)

from ppb.assetlib import Asset, ChainingMixin, AbstractAsset
from ppb.systems._sdl_utils import ttf_call


class Font(ChainingMixin, AbstractAsset):
    """
    A True-Type/OpenType Font
    """
    def __init__(self, name, *, size, index=None):
        """
        * name: the filename to load
        * size: the size in points
        * index: the index of the font in a multi-font file (rare)
        """
        # We do it this way so that the raw data can be cached between multiple
        # invocations, even though we have to reparse it every time.
        self._data = Asset(name)
        self._size = size
        self._index = index

        self._start(self._data)

    def _background(self):
        file = rw_from_object(io.BytesIO(self._data.load()))
        # ^^^^ is a pure-python emulation, does not need cleanup.
        if self._index is None:
            return ttf_call(
                TTF_OpenFontRW, file, False, self._size,
                _check_error=lambda rv: not rv
            )
        else:
            return ttf_call(
                TTF_OpenFontIndexRW, file, False, self._size, self._index,
                _check_error=lambda rv: not rv
            )

    def resize(self, size):
        """
        Returns a new copy of this font in a different size
        """
        return type(self)(self._data.name, size=size, index=self._index)
    