from ppb.vector import Vector
from ppb.engine import GameEngine

from ppb.scenes import BaseScene
from ppb.sprites import BaseSprite

import logging

def run(starting_scene=BaseScene, *, log_level=logging.WARNING, **kwargs):
    logging.basicConfig(level=log_level)
    
    with GameEngine(starting_scene, **kwargs) as eng:
        eng.run()
