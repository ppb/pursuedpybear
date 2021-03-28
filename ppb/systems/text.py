import io
import threading

from sdl2 import rw_from_object

from sdl2 import (
    SDL_FreeSurface,  # https://wiki.libsdl.org/SDL_FreeSurface
    SDL_Color,
)

from sdl2.sdlttf import (
    TTF_Init, TTF_Quit,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_6.html#SEC6
    TTF_OpenFontRW,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_15.html
    TTF_OpenFontIndexRW,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_17.html
    TTF_CloseFont,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_18.html
    TTF_FontFaceIsFixedWidth,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_34.html
    TTF_FontFaceFamilyName,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_35.html
    TTF_FontFaceStyleName,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_36.html
    TTF_RenderUTF8_Blended,  # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_52.html
)

from ppb.assetlib import Asset, ChainingMixin, AbstractAsset, FreeingMixin
from ppb.systems.sdl_utils import ttf_call

# From https://www.freetype.org/freetype2/docs/reference/ft2-base_interface.html:
# [Since 2.5.6] In multi-threaded applications it is easiest to use one
# FT_Library object per thread. In case this is too cumbersome, a single
# FT_Library object across threads is possible also, as long as a mutex lock is
# used around FT_New_Face and FT_Done_Face.
#
# I assume this translates to TTF_OpenFont* and TTF_CloseFont
# SDL_ttf manages a single global FT_Library, so we need to use the lock
# for threaded calls into it, like in Asset._background.

_freetype_lock = threading.RLock()


class Font(ChainingMixin, FreeingMixin, AbstractAsset):
    """
    A TrueType/OpenType Font
    """
    def __init__(self, name, *, size, index=None):
        """
        :param name: the filename to load
        :param size: the size in points
        :param index: the index of the font in a multi-font file (rare)
        """
        # We do it this way so that the raw data can be cached between multiple
        # invocations, even though we have to reparse it every time.
        self._data = Asset(name)
        self.size = size
        self.index = index

        self._start(self._data)

    def _background(self):
        self._file = rw_from_object(io.BytesIO(self._data.load()))
        # We have to keep the file around because freetype doesn't load
        # everything at once, resulting in segfaults.
        with _freetype_lock:
            # Doing this so that we "refcount" the FT_Library internal to SDL_ttf
            # (TTF_CloseFont is often called after system cleanup)
            ttf_call(TTF_Init, _check_error=lambda rv: rv == -1)
            if self.index is None:
                return ttf_call(
                    TTF_OpenFontRW, self._file, False, self.size,
                    _check_error=lambda rv: not rv
                )
            else:
                return ttf_call(
                    TTF_OpenFontIndexRW, self._file, False, self.size, self.index,
                    _check_error=lambda rv: not rv
                )

    def free(self, data, _TTF_CloseFont=TTF_CloseFont, _lock=_freetype_lock,
             _TTF_Quit=TTF_Quit):
        # ^^^ is a way to keep required functions during interpreter cleanup
        with _lock:
            _TTF_CloseFont(data)  # Can't fail
            _TTF_Quit()

    def __repr__(self):
        return f"<{type(self).__name__} name={self.name!r} size={self.size!r}{' loaded' if self.is_loaded() else ''} at {id(self):x}>"

    @property
    def name(self):
        return self._data.name

    def resize(self, size):
        """
        Returns a new copy of this font in a different size
        """
        return type(self)(self._data.name, size=size, index=self._index)

    @property
    def _is_fixed_width(self):
        return bool(TTF_FontFaceIsFixedWidth(self.load()))

    @property
    def _family_name(self):
        return TTF_FontFaceFamilyName(self.load())

    @property
    def _style_name(self):
        return TTF_FontFaceStyleName(self.load())


class Text(ChainingMixin, FreeingMixin, AbstractAsset):
    """
    A bit of rendered text.
    """
    def __init__(self, txt, *, font, color=(0, 0, 0)):
        """
        :param txt: The text to display.
        :param font: The font to use (a :py:class:`ppb.Font`)
        :param color: The color to use.
        """
        self.txt = txt
        self.font = font
        self.color = color

        self._start(self.font)

    def __repr__(self):
        return f"<{type(self).__name__} txt={self.txt!r} font={self.font!r} color={self.color!r}{' loaded' if self.is_loaded() else ''} at 0x{id(self):x}>"

    def _background(self):
        with _freetype_lock:
            return ttf_call(
                TTF_RenderUTF8_Blended, self.font.load(), self.txt.encode('utf-8'),
                SDL_Color(*self.color),
                _check_error=lambda rv: not rv
            )

    def free(self, object, _SDL_FreeSurface=SDL_FreeSurface):
        # ^^^ is a way to keep required functions during interpreter cleanup
        _SDL_FreeSurface(object)  # Can't fail
