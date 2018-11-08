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
        pygame.K_a: keys.A,
        pygame.K_d: keys.D,
        pygame.K_s: keys.S,
        pygame.K_w: keys.W,
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
