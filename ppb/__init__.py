from ppb.vector import Vector
from ppb.engine import GameEngine

from ppb.scenes import BaseScene
from ppb.sprites import BaseSprite


def run(starting_scene=BaseScene, **kwargs):
    with GameEngine(starting_scene, **kwargs) as eng:
        eng.run()
