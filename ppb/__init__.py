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

Exports:

* :class:`~ppb_vector.Vector`
* :class:`BaseScene`
* :class:`Circle`
* :class:`Image`
* :class:`Sprite`
* :class:`Square`
* :class:`Sound`
* :class:`Triangle`
* :mod:`events`
* :class:`Font`
* :class:`Text`
* :mod:`directions`
"""

import logging
import warnings
from typing import Callable
from typing import Union

from ppb import directions
from ppb import events
from ppb_vector import Vector
from ppb.assets import Circle
from ppb.assets import Square
from ppb.assets import Triangle
from ppb.engine import GameEngine
from ppb.scenes import BaseScene
from ppb.sprites import RectangleSprite
from ppb.sprites import Sprite
from ppb.systems import Image
from ppb.systems import Sound
from ppb.systems import Font
from ppb.systems import Text
from ppb.utils import get_time

__all__ = (
    # Shortcuts
    'Vector', 'BaseScene', 'Circle', 'Image', 'Sprite', 'RectangleSprite',
    'Square', 'Sound', 'Triangle', 'events', 'Font', 'Text', 'directions',
    # Local stuff
    'run', 'make_engine',
)


def _make_kwargs(starting_scene, title, engine_opts):
    kwargs = {
        "resolution": (800, 600),
        "first_scene": starting_scene,
        "window_title": title,
        **engine_opts
    }
    return kwargs


def run(setup: Union[Callable[[BaseScene], None], BaseScene] = lambda scene: None, *, log_level=logging.WARNING,
        starting_scene=None, scene_class=None, title="PursuedPyBear", **engine_opts):
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

    :param setup: Either a function which is called with the starting scene
       class as its only parameter, or an initalized scene ready to be
       handed to the engine.
    :type setup: Union[Callable[[BaseScene], None], BaseScene]
    :param log_level: The logging level from :func:`logging` to send to the
       console.
    :param starting_scene: Deprecated, use scene_class instead. Due for
       removal in ppb 0.12
    :type starting_scene: type
    :param title: The title of the rendered window.
    :type title: str
    :param engine_opts: Additional keyword arguments passed to the
       :class:`~ppb.engine.GameEngine`.
    """
    logging.basicConfig(level=log_level)

    if starting_scene is not None:
        warnings.warn("starting_scene parameter to ppb.run is deprecated and will be removed in version 0.12")
        if starting_scene and scene_class:
            raise ValueError("You cannot use starting_scene and scene_class together. Remove starting_scene.")
        scene_class = starting_scene
    if scene_class is None:
        scene_class = BaseScene

    if isinstance(setup, type):
        raise ValueError("setup must be either a function with one parameter `scene` or an instance of `BaseScene`.")
    elif callable(setup):
        starting_scene = scene_class()
        setup(starting_scene)
    else:
        starting_scene = setup

    with make_engine(starting_scene=starting_scene, title=title, **engine_opts) as eng:
        eng.run()


def make_engine(starting_scene=BaseScene, title="PursedPyBear",
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
    return GameEngine(**_make_kwargs(starting_scene, title, engine_opts))
