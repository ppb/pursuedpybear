import io

try:
    from pygame import mixer
except ImportError:
    mixer = None

from ppb.systemslib import System
from ppb import assetlib


class Sound(assetlib.Asset):
    def background_parse(self, data):
        if mixer is not None:
            snd = mixer.Sound(file=io.BytesIO(data))
            return snd


class SoundController(System):
    def __init__(self, **kw):
        super().__init__(**kw)

    def __enter__(self):
        if mixer is not None:
            mixer.init()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if mixer is not None:
            mixer.quit()

    def on_play_sound(self, event, signal):
        if mixer is not None:
            sound = event.sound.load()
            sound.play()
