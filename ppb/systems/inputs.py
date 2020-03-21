import ctypes
from typing import Dict

import sdl2
from sdl2 import (
    SDL_INIT_EVENTS,
    SDL_Event,  # https://wiki.libsdl.org/SDL_Event
    SDL_PollEvent,  # https://wiki.libsdl.org/SDL_PollEvent
    SDL_QUIT,  # https://wiki.libsdl.org/SDL_EventType#SDL_QUIT
    SDL_KEYDOWN, SDL_KEYUP,  # https://wiki.libsdl.org/SDL_KeyboardEvent
    SDL_MOUSEMOTION,  # https://wiki.libsdl.org/SDL_MouseMotionEvent
    SDL_BUTTON_LMASK, SDL_BUTTON_MMASK, SDL_BUTTON_RMASK,
    SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP,  # https://wiki.libsdl.org/SDL_MouseButtonEvent
    SDL_BUTTON_LEFT, SDL_BUTTON_MIDDLE, SDL_BUTTON_RIGHT,
)

import ppb.buttons as buttons
from ppb_vector import Vector
import ppb.events as events
import ppb.keycodes as keys

from ppb.systems._sdl_utils import SdlSubSystem, sdl_call


class EventPoller(SdlSubSystem):
    """
    An event poller that converts Pygame events into PPB events.
    """
    _sdl_subsystems = SDL_INIT_EVENTS

    event_map = {
        SDL_QUIT: "quit",
        SDL_MOUSEMOTION: "mouse_motion",
        SDL_MOUSEBUTTONDOWN: "button_pressed",
        SDL_MOUSEBUTTONUP: "button_released",
        SDL_KEYDOWN: "key_pressed",
        SDL_KEYUP: "key_released"
    }

    button_map: Dict[int, buttons.MouseButton] = {
        SDL_BUTTON_LEFT: buttons.Primary,
        SDL_BUTTON_MIDDLE: buttons.Tertiary,
        SDL_BUTTON_RIGHT: buttons.Secondary,
    }

    button_mask_map: Dict[int, buttons.MouseButton] = {
        SDL_BUTTON_LMASK: buttons.Primary,
        SDL_BUTTON_MMASK: buttons.Tertiary,
        SDL_BUTTON_RMASK: buttons.Secondary,
    }

    key_map: Dict[int, keys.KeyCode] = {
        sdl2.SDLK_a: keys.A,
        sdl2.SDLK_b: keys.B,
        sdl2.SDLK_c: keys.C,
        sdl2.SDLK_d: keys.D,
        sdl2.SDLK_e: keys.E,
        sdl2.SDLK_f: keys.F,
        sdl2.SDLK_g: keys.G,
        sdl2.SDLK_h: keys.H,
        sdl2.SDLK_i: keys.I,
        sdl2.SDLK_j: keys.J,
        sdl2.SDLK_k: keys.K,
        sdl2.SDLK_l: keys.L,
        sdl2.SDLK_m: keys.M,
        sdl2.SDLK_n: keys.N,
        sdl2.SDLK_o: keys.O,
        sdl2.SDLK_p: keys.P,
        sdl2.SDLK_q: keys.Q,
        sdl2.SDLK_r: keys.R,
        sdl2.SDLK_s: keys.S,
        sdl2.SDLK_t: keys.T,
        sdl2.SDLK_u: keys.U,
        sdl2.SDLK_v: keys.V,
        sdl2.SDLK_w: keys.W,
        sdl2.SDLK_x: keys.X,
        sdl2.SDLK_y: keys.Y,
        sdl2.SDLK_z: keys.Z,
        sdl2.SDLK_1: keys.One,
        sdl2.SDLK_2: keys.Two,
        sdl2.SDLK_3: keys.Three,
        sdl2.SDLK_4: keys.Four,
        sdl2.SDLK_5: keys.Five,
        sdl2.SDLK_6: keys.Six,
        sdl2.SDLK_7: keys.Seven,
        sdl2.SDLK_8: keys.Eight,
        sdl2.SDLK_9: keys.Nine,
        sdl2.SDLK_0: keys.Zero,
        sdl2.SDLK_F1: keys.F1,
        sdl2.SDLK_F2: keys.F2,
        sdl2.SDLK_F3: keys.F3,
        sdl2.SDLK_F4: keys.F4,
        sdl2.SDLK_F5: keys.F5,
        sdl2.SDLK_F6: keys.F6,
        sdl2.SDLK_F7: keys.F7,
        sdl2.SDLK_F8: keys.F8,
        sdl2.SDLK_F9: keys.F9,
        sdl2.SDLK_F10: keys.F10,
        sdl2.SDLK_F11: keys.F11,
        sdl2.SDLK_F12: keys.F12,
        sdl2.SDLK_F13: keys.F13,
        sdl2.SDLK_F14: keys.F14,
        sdl2.SDLK_F15: keys.F15,
        sdl2.SDLK_RALT: keys.AltRight,
        sdl2.SDLK_LALT: keys.AltLeft,
        sdl2.SDLK_BACKSLASH: keys.Backslash,
        sdl2.SDLK_BACKSPACE: keys.Backspace,
        sdl2.SDLK_LEFTBRACKET: keys.BracketLeft,
        sdl2.SDLK_RIGHTBRACKET: keys.BracketRight,
        sdl2.SDLK_CAPSLOCK: keys.CapsLock,
        sdl2.SDLK_COMMA: keys.Comma,
        sdl2.SDLK_LCTRL: keys.CtrlLeft,
        sdl2.SDLK_RCTRL: keys.CtrlRight,
        sdl2.SDLK_DELETE: keys.Delete,
        sdl2.SDLK_DOWN: keys.Down,
        sdl2.SDLK_END: keys.End,
        sdl2.SDLK_RETURN: keys.Enter,
        sdl2.SDLK_EQUALS: keys.Equals,
        sdl2.SDLK_ESCAPE: keys.Escape,
        sdl2.SDLK_BACKQUOTE: keys.Grave,
        sdl2.SDLK_HOME: keys.Home,
        sdl2.SDLK_INSERT: keys.Insert,
        sdl2.SDLK_LEFT: keys.Left,
        sdl2.SDLK_MENU: keys.Menu,
        sdl2.SDLK_MINUS: keys.Minus,
        sdl2.SDLK_NUMLOCKCLEAR: keys.NumLock,
        sdl2.SDLK_PAGEDOWN: keys.PageDown,
        sdl2.SDLK_PAGEUP: keys.PageUp,
        sdl2.SDLK_PAUSE: keys.Pause,
        sdl2.SDLK_PERIOD: keys.Period,
        sdl2.SDLK_PRINTSCREEN: keys.PrintScreen,
        sdl2.SDLK_QUOTE: keys.Quote,
        sdl2.SDLK_RIGHT: keys.Right,
        sdl2.SDLK_SCROLLLOCK: keys.ScrollLock,
        sdl2.SDLK_SEMICOLON: keys.Semicolon,
        sdl2.SDLK_LSHIFT: keys.ShiftLeft,
        sdl2.SDLK_RSHIFT: keys.ShiftRight,
        sdl2.SDLK_SLASH: keys.Slash,
        sdl2.SDLK_SPACE: keys.Space,
        sdl2.SDLK_LGUI: keys.SuperLeft,
        sdl2.SDLK_RGUI: keys.SuperRight,
        sdl2.SDLK_TAB: keys.Tab,
        sdl2.SDLK_UP: keys.Up,
    }

    mod_map = {
        sdl2.KMOD_LSHIFT: keys.ShiftLeft,
        sdl2.KMOD_RSHIFT: keys.ShiftRight,
        sdl2.KMOD_LCTRL: keys.CtrlLeft,
        sdl2.KMOD_RCTRL: keys.CtrlRight,
        sdl2.KMOD_LALT: keys.AltLeft,
        sdl2.KMOD_RALT: keys.AltRight,
        sdl2.KMOD_LGUI: keys.SuperLeft,
        sdl2.KMOD_RGUI: keys.SuperRight,
        sdl2.KMOD_NUM: keys.NumLock,
        sdl2.KMOD_CAPS: keys.CapsLock
    }

    def on_idle(self, idle: events.Idle, signal):
        event = SDL_Event()
        # Don't use sdl_call because no documented error return.
        # Also, inner functions do set the error flag, causing problems.
        while SDL_PollEvent(ctypes.byref(event)):
            methname = self.event_map.get(event.type)
            if methname is not None:  # Is there a handler for this pygame event?
                ppbevent = getattr(self, methname)(event, idle.scene)
                if ppbevent:  # Did the handler actually produce a ppb event?
                    signal(ppbevent)

    def quit(self, event, scene):
        return events.Quit(
            # timestamp=event.quit.timestamp,
        )

    def mouse_motion(self, event, scene):
        motion = event.motion
        screen_position = Vector(motion.x, motion.y)
        camera = scene.main_camera
        scene_position = camera.translate_to_frame(screen_position)
        delta = Vector(motion.xrel, motion.yrel) * (1/camera.pixel_ratio)
        buttons = {
            value
            for btn, value in self.button_mask_map.items()
            if motion.state & btn
        }
        return events.MouseMotion(
            position=scene_position,
            screen_position=screen_position,
            delta=delta,
            buttons=buttons,
            # timestamp=motion.timestamp
        )

    def button_pressed(self, event, scene):
        button = event.button
        screen_position = Vector(button.x, button.y)
        camera = scene.main_camera
        scene_position = camera.translate_to_frame(screen_position)
        btn = self.button_map.get(button.button)
        if btn is not None:
            return events.ButtonPressed(
                button=btn,
                position=scene_position,
                # timestamp=motion.timestamp
            )

    def button_released(self, event, scene):
        button = event.button
        screen_position = Vector(button.x, button.y)
        camera = scene.main_camera
        scene_position = camera.translate_to_frame(screen_position)
        btn = self.button_map.get(button.button)
        if btn is not None:
            return events.ButtonReleased(
                button=btn,
                position=scene_position,
                # timestamp=motion.timestamp
            )

    def key_pressed(self, event, scene):
        key = event.key
        if key.repeat:
            return
        if key.keysym.sym in self.key_map:
            return events.KeyPressed(key=self.key_map[key.keysym.sym],
                                     mods=self.build_mods(key.keysym.mod))

    def key_released(self, event, scene):
        key = event.key
        if key.repeat:
            return
        if key.keysym.sym in self.key_map:
            return events.KeyReleased(key=self.key_map[key.keysym.sym],
                                      mods=self.build_mods(key.keysym.mod))

    def build_mods(self, mods):
        return {value for mod, value in self.mod_map.items() if mod & mods}
