import logging
from typing import Callable

from ppb_vector import Vector
from ppb.engine import GameEngine
from ppb.scenes import BaseScene
from ppb.sprites import BaseSprite

__all__ = (
    # Shortcuts
    'Vector', 'BaseScene', 'BaseSprite',
    # Local stuff
    'run', 'make_engine',
)


def _make_kwargs(setup, title):
    kwargs = {
        "resolution": (800, 600),
        "scene_kwargs": {
            "set_up": setup,
        },
        "window_title": title,

    }
    return kwargs

def run(setup: Callable[[BaseScene], None]=None, *, log_level=logging.WARNING,
        starting_scene=BaseScene, title="PursuedPyBear"):
    """
    Run a small game.

    The resolution will 800 pixels wide by 600 pixels tall.

    setup is a callable that accepts a scene and returns None.

    log_level let's you set the expected log level. Consider logging.DEBUG if
    something is behaving oddly.

    starting_scene let's you change the scene used by the engine.
    """
    logging.basicConfig(level=log_level)

    with GameEngine(starting_scene, **_make_kwargs(setup, title)) as eng:
        eng.run()


def make_engine(setup: Callable[[BaseScene], None]=None, *,
                starting_scene=BaseScene, title="PursedPyBear"):
    return GameEngine(starting_scene, **_make_kwargs(setup, title))
