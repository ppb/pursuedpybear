from __future__ import division

import logging
import ctypes

import sdl2

import ppb.components.view
from ppb.event import Quit, KeyDown, KeyUp
from ppb.vmath import Vector2 as Vector
from ppb.components.models import Renderable

key_events = {sdl2.SDL_KEYUP: KeyUp,
              sdl2.SDL_KEYDOWN: KeyDown}

window = None
display = None

key_struct = None

def init(resolution, title):
    """
    Initialize sdl2 modules

    :param resolution: 2-length tuple of ints
    :param title: string
    """
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    global window
    window = sdl2.SDL_CreateWindow(title.encode("utf-8"),
                                   sdl2.SDL_WINDOWPOS_CENTERED,
                                   sdl2.SDL_WINDOWPOS_CENTERED,
                                   resolution[0],
                                   resolution[1],
                                   sdl2.SDL_WINDOW_SHOWN)
    global display
    display = sdl2.SDL_GetWindowSurface(window).contents


def quit(*_):
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()


class Keys(object):

    def __init__(self):
        self._keys = sdl2.SDL_GetKeyboardState(None)
        self.translate = {}

    def __getitem__(self, key_code):
        if key_code in self.translate:
            return self._keys[self.translate[key_code]]
        else:
            self.translate[key_code] = sdl2.SDL_GetScancodeFromKey(key_code)


def keys():
    global key_struct
    if key_struct is None:
        key_struct = Keys()
    return key_struct


def mouse():
    return {"pos": Vector(0, 0),
            "pressed": (0, 0, 0),
            "move": Vector(0, 0)
            }


def events():
    rv = []
    event = sdl2.SDL_Event()
    while sdl2.SDL_PollEvent(ctypes.byref(event)):
        if event.type == sdl2.SDL_QUIT:
            rv.append(Quit())
        elif event.type in (sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP):
            if not event.key.repeat:
                key_code = event.key.keysym.sym
                try:
                    key_name = chr(key_code)
                except ValueError:
                    key_name = ""
                rv.append(key_events[event.type](key_code, key_name))

    return rv


def render(group):
    pass


def update_screen(*_):
    sdl2.SDL_UpdateWindowSurface(window)
