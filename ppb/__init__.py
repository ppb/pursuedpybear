import logging
from typing import Callable

from ppb.vector import Vector
from ppb.engine import GameEngine
from ppb.scenes import BaseScene
from ppb.sprites import BaseSprite


def run(setup: Callable[[BaseScene], None]=None, *, log_level=logging.WARNING,
        starting_scene=BaseScene):
    """
    Run a small game.

    The resolution will 800 pixels wide by 600 pixels tall.

    setup is a callable that accepts a scene and returns None.

    log_level let's you set the expected log level. Consider logging.DEBUG if
    something is behaving oddly.

    starting_scene let's you change the scene used by the engine.
    """
    logging.basicConfig(level=log_level)

    kwargs = {
        "resolution": (800, 600),
        "scene_kwargs": {
            "set_up": setup,
        }
    }

    with GameEngine(starting_scene, **kwargs) as eng:
        eng.run()
