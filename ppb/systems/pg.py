from typing import Dict

import pygame

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

    key_map: Dict[int, keys.KeyCode] = {
        pygame.K_BACKSPACE: keys.Backspace,
        pygame.K_TAB: keys.Tab,
        pygame.K_PAUSE: keys.Pause,
        pygame.K_ESCAPE: keys.Escape,
        pygame.K_SPACE: keys.Space,
        pygame.K_QUOTE: keys.Quote,
        pygame.K_COMMA: keys.Comma,
        pygame.K_MINUS: keys.Minus,
        pygame.K_PERIOD: keys.Period,
        pygame.K_SLASH: keys.Slash,
        pygame.K_SEMICOLON: keys.Semicolon,
        pygame.K_EQUALS: keys.Equals,
        pygame.K_BACKSLASH: keys.Backslash,
        pygame.K_a: keys.A,
        pygame.K_b: keys.B,
        pygame.K_c: keys.C,
        pygame.K_d: keys.D,
        pygame.K_e: keys.E,
        pygame.K_f: keys.F,
        pygame.K_g: keys.G,
        pygame.K_h: keys.H,
        pygame.K_i: keys.I,
        pygame.K_j: keys.J,
        pygame.K_k: keys.K,
        pygame.K_l: keys.L,
        pygame.K_m: keys.M,
        pygame.K_n: keys.N,
        pygame.K_o: keys.O,
        pygame.K_p: keys.P,
        pygame.K_q: keys.Q,
        pygame.K_r: keys.R,
        pygame.K_s: keys.S,
        pygame.K_t: keys.T,
        pygame.K_u: keys.U,
        pygame.K_v: keys.V,
        pygame.K_w: keys.W,
        pygame.K_x: keys.X,
        pygame.K_y: keys.Y,
        pygame.K_z: keys.Z,
        pygame.K_DELETE: keys.Delete,
        pygame.K_UP: keys.Up,
        pygame.K_DOWN: keys.Down,
        pygame.K_RIGHT: keys.Right,
        pygame.K_LEFT: keys.Left,
        pygame.K_INSERT: keys.Insert,
        pygame.K_HOME: keys.Home,
        pygame.K_END: keys.End,
        pygame.K_PAGEUP: keys.PageUp,
        pygame.K_PAGEDOWN: keys.PageDown,
        pygame.K_F1: keys.F1,
        pygame.K_F2: keys.F2,
        pygame.K_F3: keys.F3,
        pygame.K_F4: keys.F4,
        pygame.K_F5: keys.F5,
        pygame.K_F6: keys.F6,
        pygame.K_F7: keys.F7,
        pygame.K_F8: keys.F8,
        pygame.K_F9: keys.F9,
        pygame.K_F10: keys.F10,
        pygame.K_F11: keys.F11,
        pygame.K_F12: keys.F12,
        pygame.K_F13: keys.F13,
        pygame.K_F14: keys.F14,
        pygame.K_F15: keys.F15,
        pygame.K_NUMLOCK: keys.NumLock,
        pygame.K_CAPSLOCK: keys.CapsLock,
        pygame.K_MENU: keys.Menu
    }

    def __new__(cls, *args, **kwargs):
        if cls.event_map is None:
            cls.event_map = {
                pygame.QUIT: "quit",
                pygame.MOUSEMOTION: "mouse_motion",
                pygame.MOUSEBUTTONDOWN: "button_pressed",
                pygame.MOUSEBUTTONUP: "button_released",
                pygame.KEYDOWN: "key_pressed"
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
        print("Key pressed")
        if event.key in self.key_map:
            print(f"{event.key} pressed")
            return events.KeyPressed(self.key_map[event.key]) # Mods!
