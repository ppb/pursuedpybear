from __future__ import division

import logging
import ctypes

import sdl2

import ppb.components.view
from ppb.event import Quit, KeyDown, KeyUp, MouseButtonUp, MouseButtonDown
from ppb.vmath import Vector2 as Vector
from ppb.components.models import Renderable

key_events = {sdl2.SDL_KEYUP: KeyUp,
              sdl2.SDL_KEYDOWN: KeyDown}

button_events = {sdl2.SDL_MOUSEBUTTONUP: MouseButtonUp,
                 sdl2.SDL_MOUSEBUTTONDOWN: MouseButtonDown}

button_names = {sdl2.SDL_BUTTON_LEFT: "left",
                sdl2.SDL_BUTTON_RIGHT: "right",
                sdl2.SDL_BUTTON_MIDDLE: "center"}

window = None
display = None

key_struct = None

# C Arguments
mouse_pos_x = ctypes.c_int()
mouse_pos_y = ctypes.c_int()
mouse_delta_x = ctypes.c_int()
mouse_delta_y = ctypes.c_int()


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
    bitmask = sdl2.SDL_GetMouseState(ctypes.byref(mouse_pos_x),
                                     ctypes.byref(mouse_pos_y))
    pressed = [0]
    pressed += [1 if sdl2.SDL_BUTTON(x) & bitmask else 0 for x in range(1, 4)]

    sdl2.SDL_GetRelativeMouseState(ctypes.byref(mouse_delta_x),
                                   ctypes.byref(mouse_delta_y))
    return {"pos": Vector(mouse_pos_x.value, mouse_pos_y.value),
            "pressed": tuple(pressed),
            "move": Vector(mouse_delta_x.value, mouse_delta_y.value)
            }


def events():
    rv = []
    event = sdl2.SDL_Event()
    while sdl2.SDL_PollEvent(ctypes.byref(event)):
        if event.type == sdl2.SDL_QUIT:
            rv.append(Quit())
        elif event.type in key_events:
            if not event.key.repeat:
                key_code = event.key.keysym.sym
                try:
                    key_name = chr(key_code)
                except ValueError:
                    key_name = ""
                rv.append(key_events[event.type](key_code, key_name))
        elif event.type in button_events:
            button = event.button.button
            name = button_names[button]
            pos = Vector(event.button.x, event.button.y)
            rv.append(button_events[event.type](button, name, pos))
    return rv


def render(group):
    pass


def update_screen(*_):
    sdl2.SDL_UpdateWindowSurface(window)
