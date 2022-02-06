"""
Interrogates SDL and tells us about it.
"""
import ctypes

import sdl2
from sdl2 import sdlimage
from sdl2 import sdlmixer

from ppb.systems.sdl_utils import sdl_call


def sdl_version():
    ver = sdl2.SDL_version()
    sdl_call(
        sdl2.SDL_GetVersion, ctypes.byref(ver)
    )
    return f"{ver.major}.{ver.minor}.{ver.patch}"


def sdl_revision():
    return sdl_call(sdl2.SDL_GetRevision).decode('utf-8')


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


def iter_render_drivers():
    num_drivers = sdl_call(
        sdl2.SDL_GetNumRenderDrivers,
        _check_error=lambda rv: rv <= 0
    )
    for i in range(num_drivers):
        info = sdl2.SDL_RendererInfo()
        sdl_call(
            sdl2.SDL_GetRenderDriverInfo, i, ctypes.byref(info),
            _check_error=lambda rv: rv < 0
        )
        yield info.name.decode('utf-8'), info


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


def check_audio_codecs():
    sdl2.SDL_Init(sdl2.SDL_INIT_AUDIO)
    try:
        libs = {
            'FLAC': sdlmixer.MIX_INIT_FLAC,
            'MOD': sdlmixer.MIX_INIT_MOD,
            'MP3': sdlmixer.MIX_INIT_MP3,
            'OGG': sdlmixer.MIX_INIT_OGG,
            'MIDI': sdlmixer.MIX_INIT_MID,
            'OPUS': sdlmixer.MIX_INIT_OPUS
        }
        for lib, flags in libs.items():
            sdlmixer.Mix_SetError(b"")
            ret = sdlmixer.Mix_Init(flags)
            err = sdlmixer.Mix_GetError()
            if err:
                yield lib, err.decode('utf-8')
            if ret & flags == flags:
                yield lib, None
            else:
                yield lib, True
            sdlmixer.Mix_Quit()
    finally:
        sdl2.SDL_Quit()


def check_image_codecs():
    sdl2.SDL_Init(0)
    try:
        libs = {
            'JPEG': sdlimage.IMG_INIT_JPG,
            'PNG': sdlimage.IMG_INIT_PNG,
            'TIFF': sdlimage.IMG_INIT_TIF,
            'WEBP': sdlimage.IMG_INIT_WEBP
        }
        for lib, flags in libs.items():
            sdlimage.IMG_SetError(b"")
            ret = sdlimage.IMG_Init(flags)
            err = sdlimage.IMG_GetError()
            if err:
                yield lib, err.decode('utf-8')
            if ret & flags == flags:
                yield lib, None
            else:
                yield lib, True
            sdlimage.IMG_Quit()
    finally:
        sdl2.SDL_Quit()


def iter_joysticks():
    num_sticks = sdl_call(
        sdl2.SDL_NumJoysticks,
        _check_error=lambda rv: rv < 0,
    )
    for i in range(num_sticks):
        name = sdl_call(
            sdl2.SDL_JoystickNameForIndex, i,
            _check_error=lambda rv: rv is None,
        )
        yield name.decode('utf-8')


# def iter_haptics():
#     num_sticks = sdl_call(
#         sdl2.SDL_NumHaptics,
#         _check_error=lambda rv: rv < 0,
#     )
#     for i in range(num_sticks):
#         name = sdl_call(
#             sdl2.SDL_HapticName, i,
#             _check_error=lambda rv: rv is None,
#         )
#         yield name.decode('utf-8')


def main():
    print(f"SDL Version: {sdl_version()} ({sdl_revision()})")

    print("Video Drivers:")
    for name in iter_video_drivers():
        if check_video_driver(name):
            print(f" y {name}")
        else:
            print(f" n {name}")

    print("Renderers:")
    for name, _ in iter_render_drivers():
        print(f" * {name}")

    print("Audio Drivers:")
    for name in iter_audio_drivers():
        if check_audio_driver(name):
            print(f" y {name}")
        else:
            print(f" n {name}")

    print("Image Codecs:")
    for name, err in check_image_codecs():
        if err is None:
            print(f" y {name}")
        elif err is True:
            print(f" n {name}")
        else:
            print(f" n {name} ({err})")

    print("Audio Codecs:")
    for name, err in check_audio_codecs():
        if err is None:
            print(f" y {name}")
        elif err is True:
            print(f" n {name}")
        else:
            print(f" n {name} ({err})")

    print("Joysticks:")
    for name in iter_joysticks():
        print(f" * {name}")

    # print("Haptics:")
    # for name in iter_haptics():
    #     print(f" * {name}")


if __name__ == '__main__':
    main()
