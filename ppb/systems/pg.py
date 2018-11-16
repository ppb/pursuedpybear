from typing import Dict

import pygame
import pygame.constants

import ppb.buttons as buttons
from ppb import Vector
from ppb import events
from ppb import keycodes as keys
from ppb.systems import System  # TODO: Be aware of circular imports
from ppb.systems import default_resolution


class EventPoller(System):
    """
    An event poller that converts Pygame events into PPB events.
    """

    event_map = None

    button_map = {
        1: buttons.Primary,
        2: buttons.Tertiary,
        3: buttons.Secondary,
    }

    key_map = {
        pygame.constants.K_a: keys.A,
        pygame.constants.K_b: keys.B,
        pygame.constants.K_c: keys.C,
        pygame.constants.K_d: keys.D,
        pygame.constants.K_e: keys.E,
        pygame.constants.K_f: keys.F,
        pygame.constants.K_g: keys.G,
        pygame.constants.K_h: keys.H,
        pygame.constants.K_i: keys.I,
        pygame.constants.K_j: keys.J,
        pygame.constants.K_k: keys.K,
        pygame.constants.K_l: keys.L,
        pygame.constants.K_m: keys.M,
        pygame.constants.K_n: keys.N,
        pygame.constants.K_o: keys.O,
        pygame.constants.K_p: keys.P,
        pygame.constants.K_q: keys.Q,
        pygame.constants.K_r: keys.R,
        pygame.constants.K_s: keys.S,
        pygame.constants.K_t: keys.T,
        pygame.constants.K_u: keys.U,
        pygame.constants.K_v: keys.V,
        pygame.constants.K_w: keys.W,
        pygame.constants.K_x: keys.X,
        pygame.constants.K_y: keys.Y,
        pygame.constants.K_z: keys.Z,
        pygame.constants.K_1: keys.One,
        pygame.constants.K_2: keys.Two,
        pygame.constants.K_3: keys.Three,
        pygame.constants.K_4: keys.Four,
        pygame.constants.K_5: keys.Five,
        pygame.constants.K_6: keys.Six,
        pygame.constants.K_7: keys.Seven,
        pygame.constants.K_8: keys.Eight,
        pygame.constants.K_9: keys.Nine,
        pygame.constants.K_0: keys.Zero,
        pygame.constants.K_F1: keys.F1,
        pygame.constants.K_F2: keys.F2,
        pygame.constants.K_F3: keys.F3,
        pygame.constants.K_F4: keys.F4,
        pygame.constants.K_F5: keys.F5,
        pygame.constants.K_F6: keys.F6,
        pygame.constants.K_F7: keys.F7,
        pygame.constants.K_F8: keys.F8,
        pygame.constants.K_F9: keys.F9,
        pygame.constants.K_F10: keys.F10,
        pygame.constants.K_F11: keys.F11,
        pygame.constants.K_F12: keys.F12,
        pygame.constants.K_F13: keys.F13,
        pygame.constants.K_F14: keys.F14,
        pygame.constants.K_F15: keys.F15,
        pygame.constants.K_RALT: keys.AltRight,
        pygame.constants.K_LALT: keys.AltLeft,
        pygame.constants.K_BACKSLASH: keys.Backslash,
        pygame.constants.K_BACKSPACE: keys.Backspace,
        pygame.constants.K_LEFTBRACKET: keys.BracketLeft,
        pygame.constants.K_RIGHTBRACKET: keys.BracketRight,
        pygame.constants.K_CAPSLOCK: keys.CapsLock,
        pygame.constants.K_COMMA: keys.Comma,
        pygame.constants.K_LCTRL: keys.CtrlLeft,
        pygame.constants.K_RCTRL: keys.CtrlRight,
        pygame.constants.K_DELETE: keys.Delete,
        pygame.constants.K_DOWN: keys.Down,
        pygame.constants.K_END: keys.End,
        pygame.constants.K_RETURN: keys.Enter,
        pygame.constants.K_EQUALS: keys.Equals,
        pygame.constants.K_ESCAPE: keys.Escape,
        pygame.constants.K_BACKQUOTE: keys.Grave,
        pygame.constants.K_HOME: keys.Home,
        pygame.constants.K_INSERT: keys.Insert,
        pygame.constants.K_LEFT: keys.Left,
        pygame.constants.K_MENU: keys.Menu,
        pygame.constants.K_MINUS: keys.Minus,
        pygame.constants.K_NUMLOCK: keys.NumLock,
        pygame.constants.K_PAGEDOWN: keys.PageDown,
        pygame.constants.K_PAGEUP: keys.PageUp,
        pygame.constants.K_PAUSE: keys.Pause,
        pygame.constants.K_BREAK: keys.Pause,
        pygame.constants.K_PERIOD: keys.Period,
        pygame.constants.K_PRINT: keys.PrintScreen,
        pygame.constants.K_QUOTE: keys.Quote,
        pygame.constants.K_RIGHT: keys.Right,
        pygame.constants.K_SCROLLOCK: keys.ScrollLock,
        pygame.constants.K_SEMICOLON: keys.Semicolon,
        pygame.constants.K_LSHIFT: keys.ShiftLeft,
        pygame.constants.K_RSHIFT: keys.ShiftRight,
        pygame.constants.K_SLASH: keys.Slash,
        pygame.constants.K_SPACE: keys.Space,
        pygame.constants.K_LSUPER: keys.SuperLeft,
        pygame.constants.K_LMETA: keys.SuperLeft,
        pygame.constants.K_RSUPER: keys.SuperRight,
        pygame.constants.K_RMETA: keys.SuperRight,
        pygame.constants.K_TAB: keys.Tab,
        pygame.constants.K_UP: keys.Up,
    }

    mod_map = {
        pygame.constants.KMOD_LSHIFT: keys.ShiftLeft,
        pygame.constants.KMOD_RSHIFT: keys.ShiftRight,
        pygame.constants.KMOD_LCTRL: keys.CtrlLeft,
        pygame.constants.KMOD_RCTRL: keys.CtrlRight,
        pygame.constants.KMOD_LALT: keys.AltLeft,
        pygame.constants.KMOD_RALT: keys.AltRight,
        pygame.constants.KMOD_LMETA: keys.SuperLeft,
        pygame.constants.KMOD_RMETA: keys.SuperRight,
        pygame.constants.KMOD_NUM: keys.NumLock,
        pygame.constants.KMOD_CAPS: keys.CapsLock
    }

    def __new__(cls, *args, **kwargs):
        if cls.event_map is None:
            cls.event_map = {
                pygame.QUIT: "quit",
                pygame.MOUSEMOTION: "mouse_motion",
                pygame.MOUSEBUTTONDOWN: "button_pressed",
                pygame.MOUSEBUTTONUP: "button_released",
                pygame.KEYDOWN: "key_pressed",
                pygame.KEYUP: "key_released"
            }
        return super().__new__(cls)

    def __init__(self, resolution=default_resolution, **kwargs):  # TODO: Resolve default locations
        self.offset = Vector(-0.5 * resolution[0],
                             -0.5 * resolution[1])

    def __enter__(self):
        pygame.init()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def on_update(self, update, signal):
        for pygame_event in pygame.event.get():
            methname = self.event_map.get(pygame_event.type)
            if methname is not None:  # Is there a handler for this pygame event?
                ppbevent = getattr(self, methname)(pygame_event, update.scene)
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
