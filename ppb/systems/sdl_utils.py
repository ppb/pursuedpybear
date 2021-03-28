import atexit

from sdl2 import (
    SDL_GetError,   # https://wiki.libsdl.org/SDL_GetError
    SDL_ClearError,  # https://wiki.libsdl.org/SDL_ClearError
    SDL_InitSubSystem,  # https://wiki.libsdl.org/SDL_InitSubSystem
    SDL_QuitSubSystem,  # https://wiki.libsdl.org/SDL_QuitSubSystem
    SDL_Quit,  # https://wiki.libsdl.org/SDL_Quit
)

from sdl2.sdlmixer import (
    # Errors, https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_7.html#SEC7
    Mix_GetError, Mix_SetError,
)

from sdl2.sdlimage import (
    IMG_GetError, IMG_SetError,  # https://www.libsdl.org/projects/SDL_image/docs/SDL_image_43.html#SEC43
)

from sdl2.sdlttf import (
    # https://www.libsdl.org/projects/SDL_ttf/docs/SDL_ttf_6.html#SEC6
    TTF_GetError, TTF_SetError,
)


from ppb.systemslib import System


atexit.register(SDL_Quit)
# The PPB model makes it hard to register this in connection with the actual
# engine cleanup, so we'll do it on interpreter exit.


class SdlError(Exception):
    """
    SDL raised an error
    """


def sdl_call(func, *pargs, _check_error=None, **kwargs):
    """
    Wrapper for calling SDL functions for handling errors.

    If _check_error is given, called with the return value to check for errors.
    If _check_error returns truthy, an error occurred.

    If _check_error is not given, it is assumed that a non-empty error from
    Mix_GetError indicates error.
    """
    SDL_ClearError()
    rv = func(*pargs, **kwargs)
    err = SDL_GetError()
    if (_check_error(rv) if _check_error else err):
        raise SdlError(f"Error calling {func.__name__}: {err.decode('utf-8')}")
    else:
        return rv


class SdlSubSystem(System):
    """
    Handles SDL_InitSubSystem/SDL_QuitSubSystem
    """
    _sdl_subsystems = 0

    def __enter__(self):
        super().__enter__()
        sdl_call(SDL_InitSubSystem, self._sdl_subsystems, _check_error=lambda rv: rv < 0)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sdl_call(SDL_QuitSubSystem, self._sdl_subsystems)
        super().__exit__(exc_type, exc_val, exc_tb)


class SdlMixerError(SdlError):
    """
    SDL_mixer raised an error
    """


def mix_call(func, *pargs, _check_error=None, **kwargs):
    """
    Wrapper for calling SDL_mixer functions for handling errors.

    If _check_error is given, called with the return value to check for errors.
    If _check_error returns truthy, an error occurred.

    If _check_error is not given, it is assumed that a non-empty error from
    Mix_GetError indicates error.
    """
    Mix_SetError(b"")
    rv = func(*pargs, **kwargs)
    err = Mix_GetError()
    if (_check_error(rv) if _check_error else err):
        raise SdlMixerError(f"Error calling {func.__name__}: {err.decode('utf-8')}")
    else:
        return rv


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


class TtfError(SdlError):
    pass


def ttf_call(func, *pargs, _check_error=None, **kwargs):
    """
    Wrapper for calling SDL functions for handling errors.

    If _check_error is given, called with the return value to check for errors.
    If _check_error returns truthy, an error occurred.

    If _check_error is not given, it is assumed that a non-empty error from
    Mix_GetError indicates error.
    """
    TTF_SetError(b"")
    rv = func(*pargs, **kwargs)
    err = TTF_GetError()
    if (_check_error(rv) if _check_error else err):
        raise SdlError(f"Error calling {func.__name__}: {err.decode('utf-8')}")
    else:
        return rv
