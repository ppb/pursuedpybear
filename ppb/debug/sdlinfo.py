"""
Interrogates SDL and tells us about it.
"""
import ctypes

import sdl2
from sdl2 import SDL_Init, SDL_Quit
from sdl2 import sdlmixer

from ppb.systems.sdl_utils import sdl_call


def sdl_version():
    ver = sdl2.SDL_version()
    sdl_call(
        sdl2.SDL_GetVersion, ctypes.byref(ver)
    )
    rev = sdl_call(sdl2.SDL_GetRevision).decode('utf-8')
    return f"{ver.major}.{ver.minor}.{ver.patch}+{rev}"


def iter_video_drivers():
    num_drivers = sdl_call(
        sdl2.SDL_GetNumVideoDrivers,
        _check_error=lambda rv: rv <= 0
    )
    for i in range(num_drivers):
        yield sdl_call(sdl2.SDL_GetVideoDriver, i).decode('utf-8')


def check_video_driver(name):
    try:
        sdl_call(
            sdl2.SDL_VideoInit, name.encode('utf-8'),
            _check_error=lambda rv: rv < 0
        )
    except Exception:
        return False
    else:
        sdl_call(
            sdl2.SDL_VideoQuit, name,
        )
        return True


def iter_audio_drivers():
    num_drivers = sdl_call(
        sdl2.SDL_GetNumAudioDrivers,
    )
    for i in range(num_drivers):
        yield sdl_call(
            sdl2.SDL_GetAudioDriver, i,
            _check_error=lambda rv: rv is None,
        ).decode('utf-8')


def check_audio_driver(name):
    try:
        sdl_call(
            sdl2.SDL_AudioInit, name.encode('utf-8'),
            _check_error=lambda rv: rv < 0
        )
    except Exception:
        return False
    else:
        sdl_call(
            sdl2.SDL_AudioQuit, name,
        )
        return True


def main():
    print("SDL Version:", sdl_version())


    print("Video Drivers:")
    for name in iter_video_drivers():
        if check_video_driver(name):
            print(f" y {name}")
        else:
            print(f" n {name}")


    print("Audio Drivers:")
    for name in iter_audio_drivers():
        if check_audio_driver(name):
            print(f" y {name}")
        else:
            print(f" n {name}")


# SDL_Init(sdl2.SDL_INIT_AUDIO)
# supported = []
# libs = {
#     'FLAC': sdlmixer.MIX_INIT_FLAC,
#     'MOD': sdlmixer.MIX_INIT_MOD,
#     'MP3': sdlmixer.MIX_INIT_MP3,
#     'OGG': sdlmixer.MIX_INIT_OGG,
#     'MID': sdlmixer.MIX_INIT_MID,
#     'OPUS': sdlmixer.MIX_INIT_OPUS
# }
# for lib in libs.keys():
#     flags = libs[lib]
#     ret = sdlmixer.Mix_Init(flags)
#     err = sdlmixer.Mix_GetError()
#     if err:
#         print("Error for {0}: {1}".format(lib, err))
#     if ret & flags == flags:
#         supported.append(lib)
#     sdlmixer.Mix_Quit()
# print("Supported formats:")
# print(supported)
# SDL_Quit()


if __name__ == '__main__':
    main()
