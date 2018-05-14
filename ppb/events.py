import weakref
import collections
import logging
import typing
import re
from .dataclasses import dataclass
from .abc import Scene

__all__ = (
    'EventMixin',
    'Update',
)


def camel_to_snake(txt):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', txt)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class EventMixin:
    def __event__(self, bag, fire_event):
        elog = logging.getLogger('game.events')

        name = camel_to_snake(type(bag).__name__)

        meth = getattr(self, 'on_' + name, None)
        if meth and callable(meth):
            elog.debug(f"Calling handler {meth} for {name}")
            meth(bag, scene, fire_event)


# Remember to define scene at the end so the pargs version of __init__() still works


@dataclass()
class Update:
    """
    Fired on game tick
    """
    time_delta: float
    scene: Scene = None


@dataclass()
class Prerender:
    """
    TODO
    """
    scene: Scene = None
