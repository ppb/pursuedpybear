"""
A python game framework.

PursuedPyBear is object oriented and event driven. Practically, this means that
most of your code will be organized into classes. Game objects in
:mod:`ppb` are :class:`Sprite` instances, which get contained in
:class:`BaseScenes <BaseScene>`. In turn, the :class:`GameEngine`
contains the scenes and :class:`Systems <System>`.
:mod:`Events <events>` are defined as simple classes and event handlers
are based on their names.

The classes, modules, and methods exported directly are the most used parts of
the library and intended to be used by users at all levels (barring
make_engine). Advanced features tend to be in their own modules and subpackages.
"""

import logging
import warnings
from typing import Callable

from ppb import events
from ppb_vector import Vector
from ppb.assets import Circle
from ppb.assets import Square
from ppb.assets import Triangle
from ppb.engine import GameEngine
from ppb.scenes import BaseScene
from ppb.sprites import Sprite
from ppb.systems import Image
from ppb.systems import Sound
from ppb.systems import Font
from ppb.systems import Text

__all__ = (
    # Shortcuts
    'Vector', 'BaseScene', 'BaseSprite', 'Circle', 'Image', 'Sprite',
    'Square', 'Sound', 'Triangle', 'events', 'Font', 'Text',
    # Local stuff
    'run', 'make_engine',
)


class BaseSprite(Sprite):
    """
    A stub that raises a deprecation warning when a user uses
    ``ppb.BaseSprite.``
    """
    __warning = """Using ppb.BaseSprite is deprecated.

    You probably want ppb.Sprite. If you're wanting to use BaseSprite and
    mixins to change what features your sprites have, import
    ppb.sprites.BaseSprite.
    """

    def __init__(self, **kwargs):
        warnings.warn(self.__warning, DeprecationWarning)
        super().__init__(**kwargs)


def _make_kwargs(setup, title, engine_opts):
    kwargs = {
        "resolution": (800, 600),
        "scene_kwargs": {
            "set_up": setup,
        },
        "window_title": title,
        **engine_opts
    }
    return kwargs


def run(setup: Callable[[BaseScene], None] = None, *, log_level=logging.WARNING,
        starting_scene=BaseScene, title="PursuedPyBear", **engine_opts):
    """
    Run a game.

    This is the default entry point for ppb games.

    Sample usage:
    ::
       import ppb

       def setup(scene):
           scene.add(ppb.Sprite())

       ppb.run(setup)

    Alternatively:
    ::
       import ppb

       class Game(ppb.BaseScene):
           def __init__(self, **kwargs):
               super().__init__(**kwargs)
               self.add(ppb.Sprite())

       ppb.run(starting_scene=Game)

    See the :doc:`../getting-started` guide for a more complete guide to
    building games.

    All parameters are optional.

    :param setup: Called with the first scene to allow initialization of
       your game.
    :type setup: Callable[[BaseScene], None]
    :param log_level: The logging level from :func:`logging` to send to the
       console.
    :param starting_scene: A scene class to use. Defaults to
       :class:`~ppb.scenes.BaseScene`
    :type starting_scene: type
    :param title: The title of the rendered window.
    :type title: str
    :param engine_opts: Additional keyword arguments passed to the
       :class:`~ppb.engine.GameEngine`.
    """
    logging.basicConfig(level=log_level)

    with make_engine(setup, starting_scene=starting_scene, title=title, **engine_opts) as eng:
        eng.run()


def make_engine(setup: Callable[[BaseScene], None] = None, *,
                starting_scene=BaseScene, title="PursedPyBear",
                **engine_opts):
    """
    Setup a :class:`GameEngine`.

    This function exists for third party modules to use the same code paths
    as :func:`run` for setting up their engine. If you want to instantiate
    your own engine, you can do so directly using the
    :class:`constructor <GameEngine>`.

    :param setup: Called with the first scene to allow initialization of
       your game.
    :type setup: Callable[[BaseScene], None]
    :param starting_scene: A scene class to use. Defaults to
       :class:`~ppb.scenes.BaseScene`
    :type starting_scene: type
    :param title: The title of the rendered window.
    :type title: str
    :param engine_opts: Additional keyword arguments passed to the
       :class:`~ppb.engine.GameEngine`
    :return: A GameEngine instance.
    """
    return GameEngine(starting_scene, **_make_kwargs(setup, title, engine_opts))
