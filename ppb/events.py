from dataclasses import dataclass
import logging
import re
from typing import Iterable

from ppb.abc import Scene
from ppb.vector import Vector

__all__ = (
    'EventMixin',
    'PreRender',
    'Quit',
    'Render',
    'Update',
)

boundaries_finder = re.compile('(.)([A-Z][a-z]+)')
boundaries_finder_2 = re.compile('([a-z0-9])([A-Z])')

def camel_to_snake(txt):
    s1 = boundaries_finder.sub(r'\1_\2', txt)
    return boundaries_finder_2.sub(r'\1_\2', s1).lower()


class EventMixin:
    def __event__(self, bag, fire_event):
        elog = logging.getLogger('game.events')

        name = camel_to_snake(type(bag).__name__)

        meth = getattr(self, 'on_' + name, None)
        if callable(meth):
            elog.debug(f"Calling handler {meth} for {name}")
            meth(bag, fire_event)


# Remember to define scene at the end so the pargs version of __init__() still works

@dataclass
class MouseMotion:
    """An event to represent mouse motion."""
    position: Vector
    delta: Vector
    buttons: Iterable
    scene: Scene = None


@dataclass
class PreRender:
    """
    Fired before rendering.
    """
    scene: Scene = None


@dataclass
class Quit:
    """
    Fired on an OS Quit event.
    """
    scene: Scene = None


@dataclass
class Render:
    """
    Fired at render.
    """
    scene: Scene = None


@dataclass
class Update:
    """
    Fired on game tick
    """
    time_delta: float
    scene: Scene = None
