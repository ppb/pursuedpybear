import weakref
import collections
import logging
import typing
from .dataclasses import dataclass
from .abc import Scene

__all__ = (
    'EventMixin', 'fire_event',
    'UpdateEvent',
)

_registrations = collections.defaultdict(set)


class EventMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _register_instance(self)


def _register_instance(obj: EventMixin):
    global _registrations
    for name in dir(obj):
        if not name.startswith('on_'):
            continue
        event = name[len('on_'):]
        val = getattr(obj, name)
        if callable(val):
            _registrations[event].add(weakref.WeakMethod(val))


def fire_event(name: str, bag: object, scene: Scene):
    callback = lambda name, bag: fire_event(name, bag, scene)

    log = logging.getLogger('events')

    for func in _registrations[name]:
        try:
            func()(bag, scene, callback)
        except Exception:
            log.exception("Error in event handler")


@dataclass()
class UpdateEvent:
    """
    Fired on game tick
    """
    time_delta: float
