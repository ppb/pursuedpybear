from ppb.vector import Vector
from ppb.engine import GameEngine

from ppb.scenes import BaseScene
from ppb.sprites import BaseSprite

import logging
import pyglet

def run(starting_scene=BaseScene, *, log_level=logging.WARNING, **kwargs):
    logging.basicConfig(level=log_level)
    
    eng = GameEngine(starting_scene, **kwargs)
    pyglet.app.event_loop = eng
    eng.run()
