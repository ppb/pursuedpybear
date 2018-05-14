import weakref
import collections
import logging
import typing
from .dataclasses import dataclass
from .abc import Scene

__all__ = (
    'EventMixin',
    # EventSystem is public but not a default import
    'UpdateEvent',
)

class EventMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class EventSystem:
    def __init__(self):
        self.registrations = collections.defaultdict(set)

    def register_object(self, obj: EventMixin):
        for name in dir(obj):
            if not name.startswith('on_'):
                continue
            event = name[len('on_'):]
            val = getattr(obj, name)
            if callable(val):
                self.registrations[event].add(weakref.WeakMethod(val))

    def fire_event(self, name: str, bag: object, scene: Scene):
        """
        Fire an event, executing its handlers.
        """
        callback = lambda name, bag: self.fire_event(name, bag, scene)

        elog = logging.getLogger('events')
        ppblog = logging.getLogger('ppb.events')

        if scene is None:
            ppblog.warning(f"Event {name} fired with no scene")
            return

        for func in self.registrations[name]:
            try:
                func()(bag, scene, callback)
            except Exception:
                elog.exception("Error in event handler")


@dataclass()
class UpdateEvent:
    """
    Fired on game tick
    """
    time_delta: float
