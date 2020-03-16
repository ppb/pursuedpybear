import ctypes
from typing import Dict

from sdl2 import (
    SDL_INIT_EVENTS,
    SDL_Event,  # https://wiki.libsdl.org/SDL_Event
    SDL_PollEvent,  # https://wiki.libsdl.org/SDL_PollEvent
    SDL_QUIT,  # https://wiki.libsdl.org/SDL_EventType#SDL_QUIT
    SDL_KEYDOWN, SDL_KEYUP,  # https://wiki.libsdl.org/SDL_KeyboardEvent
    SDL_MOUSEMOTION,  # https://wiki.libsdl.org/SDL_MouseMotionEvent
    SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP,  # https://wiki.libsdl.org/SDL_MouseButtonEvent
    SDL_BUTTON_LEFT, SDL_BUTTON_MIDDLE, SDL_BUTTON_RIGHT,
)

import ppb.buttons as buttons
from ppb_vector import Vector
import ppb.events as events
import ppb.keycodes as keys
from ppb.systems.renderer import DEFAULT_RESOLUTION

from ppb.systems._sdl_utils import SdlSubSystem, sdl_call


class EventPoller(SdlSubSystem):
    """
    An event poller that converts Pygame events into PPB events.
    """
    _subsystems = SDL_INIT_EVENTS

    event_map = {
        SDL_QUIT: "quit",
        # SDL_MOUSEMOTION: "mouse_motion",
        # SDL_MOUSEBUTTONDOWN: "button_pressed",
        # SDL_MOUSEBUTTONUP: "button_released",
        # SDL_KEYDOWN: "key_pressed",
        # SDL_KEYUP: "key_released"
    }

    button_map: Dict[int, buttons.MouseButton] = {
        SDL_BUTTON_LEFT: buttons.Primary,
        SDL_BUTTON_MIDDLE: buttons.Tertiary,
        SDL_BUTTON_RIGHT: buttons.Secondary,
    }

    key_map: Dict[int, keys.KeyCode] = {
        # pygame.K_a: keys.A,
        # pygame.K_b: keys.B,
        # pygame.K_c: keys.C,
        # pygame.K_d: keys.D,
        # pygame.K_e: keys.E,
        # pygame.K_f: keys.F,
        # pygame.K_g: keys.G,
        # pygame.K_h: keys.H,
        # pygame.K_i: keys.I,
        # pygame.K_j: keys.J,
        # pygame.K_k: keys.K,
        # pygame.K_l: keys.L,
        # pygame.K_m: keys.M,
        # pygame.K_n: keys.N,
        # pygame.K_o: keys.O,
        # pygame.K_p: keys.P,
        # pygame.K_q: keys.Q,
        # pygame.K_r: keys.R,
        # pygame.K_s: keys.S,
        # pygame.K_t: keys.T,
        # pygame.K_u: keys.U,
        # pygame.K_v: keys.V,
        # pygame.K_w: keys.W,
        # pygame.K_x: keys.X,
        # pygame.K_y: keys.Y,
        # pygame.K_z: keys.Z,
        # pygame.K_1: keys.One,
        # pygame.K_2: keys.Two,
        # pygame.K_3: keys.Three,
        # pygame.K_4: keys.Four,
        # pygame.K_5: keys.Five,
        # pygame.K_6: keys.Six,
        # pygame.K_7: keys.Seven,
        # pygame.K_8: keys.Eight,
        # pygame.K_9: keys.Nine,
        # pygame.K_0: keys.Zero,
        # pygame.K_F1: keys.F1,
        # pygame.K_F2: keys.F2,
        # pygame.K_F3: keys.F3,
        # pygame.K_F4: keys.F4,
        # pygame.K_F5: keys.F5,
        # pygame.K_F6: keys.F6,
        # pygame.K_F7: keys.F7,
        # pygame.K_F8: keys.F8,
        # pygame.K_F9: keys.F9,
        # pygame.K_F10: keys.F10,
        # pygame.K_F11: keys.F11,
        # pygame.K_F12: keys.F12,
        # pygame.K_F13: keys.F13,
        # pygame.K_F14: keys.F14,
        # pygame.K_F15: keys.F15,
        # pygame.K_RALT: keys.AltRight,
        # pygame.K_LALT: keys.AltLeft,
        # pygame.K_BACKSLASH: keys.Backslash,
        # pygame.K_BACKSPACE: keys.Backspace,
        # pygame.K_LEFTBRACKET: keys.BracketLeft,
        # pygame.K_RIGHTBRACKET: keys.BracketRight,
        # pygame.K_CAPSLOCK: keys.CapsLock,
        # pygame.K_COMMA: keys.Comma,
        # pygame.K_LCTRL: keys.CtrlLeft,
        # pygame.K_RCTRL: keys.CtrlRight,
        # pygame.K_DELETE: keys.Delete,
        # pygame.K_DOWN: keys.Down,
        # pygame.K_END: keys.End,
        # pygame.K_RETURN: keys.Enter,
        # pygame.K_EQUALS: keys.Equals,
        # pygame.K_ESCAPE: keys.Escape,
        # pygame.K_BACKQUOTE: keys.Grave,
        # pygame.K_HOME: keys.Home,
        # pygame.K_INSERT: keys.Insert,
        # pygame.K_LEFT: keys.Left,
        # pygame.K_MENU: keys.Menu,
        # pygame.K_MINUS: keys.Minus,
        # pygame.K_NUMLOCK: keys.NumLock,
        # pygame.K_PAGEDOWN: keys.PageDown,
        # pygame.K_PAGEUP: keys.PageUp,
        # pygame.K_PAUSE: keys.Pause,
        # pygame.K_BREAK: keys.Pause,
        # pygame.K_PERIOD: keys.Period,
        # pygame.K_PRINT: keys.PrintScreen,
        # pygame.K_QUOTE: keys.Quote,
        # pygame.K_RIGHT: keys.Right,
        # pygame.K_SCROLLOCK: keys.ScrollLock,
        # pygame.K_SEMICOLON: keys.Semicolon,
        # pygame.K_LSHIFT: keys.ShiftLeft,
        # pygame.K_RSHIFT: keys.ShiftRight,
        # pygame.K_SLASH: keys.Slash,
        # pygame.K_SPACE: keys.Space,
        # pygame.K_LSUPER: keys.SuperLeft,
        # pygame.K_LMETA: keys.SuperLeft,
        # pygame.K_RSUPER: keys.SuperRight,
        # pygame.K_RMETA: keys.SuperRight,
        # pygame.K_TAB: keys.Tab,
        # pygame.K_UP: keys.Up,
    }

    mod_map = {
        # pygame.KMOD_LSHIFT: keys.ShiftLeft,
        # pygame.KMOD_RSHIFT: keys.ShiftRight,
        # pygame.KMOD_LCTRL: keys.CtrlLeft,
        # pygame.KMOD_RCTRL: keys.CtrlRight,
        # pygame.KMOD_LALT: keys.AltLeft,
        # pygame.KMOD_RALT: keys.AltRight,
        # pygame.KMOD_LMETA: keys.SuperLeft,
        # pygame.KMOD_RMETA: keys.SuperRight,
        # pygame.KMOD_NUM: keys.NumLock,
        # pygame.KMOD_CAPS: keys.CapsLock
    }

    def __init__(self, resolution=DEFAULT_RESOLUTION, **kwargs):  # TODO: Resolve default locations
        self.offset = Vector(-0.5 * resolution[0],
                             -0.5 * resolution[1])

    def on_idle(self, idle: events.Idle, signal):
        event = SDL_Event()
        while sdl_call(SDL_PollEvent, ctypes.byref(event)):
            methname = self.event_map.get(event.type)
            if methname is not None:  # Is there a handler for this pygame event?
                ppbevent = getattr(self, methname)(event, idle.scene)
                if ppbevent:  # Did the handler actually produce a ppb event?
                    signal(ppbevent)

    def quit(self, event, scene):
        return events.Quit()

    def mouse_motion(self, event, scene):
        screen_position = Vector(*event.pos)
        camera = scene.main_camera
        scene_position = camera.translate_to_frame(screen_position)
        delta = Vector(*event.rel) * (1/camera.pixel_ratio)
        buttons = {
            self.button_map[btn+1]
            for btn, value in enumerate(event.buttons)
            if value
        }
        return events.MouseMotion(
            position=scene_position,
            screen_position=screen_position,
            delta=delta,
            buttons=buttons)

    def button_pressed(self, event, scene):
        screen_position = Vector(*event.pos)
        camera = scene.main_camera
        scene_position = camera.translate_to_frame(screen_position)
        btn = self.button_map.get(event.button)
        if btn is not None:
            return events.ButtonPressed(
                button=btn,
                position=scene_position,
                # TODO: Add frame position
            )

    def button_released(self, event, scene):
        screen_position = Vector(*event.pos)
        camera = scene.main_camera
        scene_position = camera.translate_to_frame(screen_position)
        btn = self.button_map.get(event.button)
        if btn is not None:
            return events.ButtonReleased(
                button=btn,
                position=scene_position,
                # TODO: Add frame position
            )

    def key_pressed(self, event, scene):
        if event.key in self.key_map:
            return events.KeyPressed(key=self.key_map[event.key],
                                     mods=self.build_mods(event))

    def key_released(self, event, scene):
        if event.key in self.key_map:
            return events.KeyReleased(key=self.key_map[event.key],
                                      mods=self.build_mods(event))

    def build_mods(self, event):
        return {value for mod, value in self.mod_map.items() if mod & event.mod}
