from ppb.vector import Vector
from ppb.engine import GameEngine

from ppb.sprites import BaseSprite
# Needs to come after BaseSprite because it technically depends on it.
from ppb.scenes import BaseScene



def run(starting_scene=BaseScene, **kwargs):
    with GameEngine(starting_scene, **kwargs) as eng:
        eng.run()
