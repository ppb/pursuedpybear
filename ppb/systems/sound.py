import io

import pygame.mixer

from ppb.systemslib import System
from ppb import assets


class Sound(assets.Asset):
    def background_parse(self, data):
        snd = pygame.mixer.Sound(file=io.BytesIO(data))
        return snd


class SoundController(System):
    def __init__(self, **kw):
        super().__init__(**kw)

    def __enter__(self):
        pygame.mixer.init()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.mixer.quit()

    def on_play_sound(self, event, signal):
        sound = event.sound.load()
        sound.play()
