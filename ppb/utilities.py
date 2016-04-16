from __future__ import division

from collections import defaultdict
from event import Tick
import logging

from ppb.vmath import Vector2 as Vector


class FollowCam(object):

    def __init__(self, target, resolution, max_dist=50, max_speed=10.0):
        self.pos = Vector(*target.pos)
        self.target = target
        self.max_distance = max_dist
        self.speed = max_speed
        self.offset = Vector(*resolution) * .5

    def update(self, td):
        direction = self.target.pos - self.pos
        distance = direction.length
        direction = direction.normalize()
        if distance > self.max_distance:
            self.pos += direction * self.speed * td

    def get_offset(self):
        return self.pos - self.offset


class Publisher(object):
    """
    A generic publisher class.
    """

    def __init__(self, dispatcher=None):
        """
        Create publisher.

        :param dispatcher: Publisher
        :return: Publisher
        """
        self.subscribers = defaultdict(set)
        self.subscribe_requests = []
        self.dispatcher = dispatcher
        self.unsubscribe_requests = []

    def publish(self, event):
        """
        Publish an event to subscribers.

        :param event: An Event to publish
        :return: None
        """
        if self.unsubscribe_requests:
            self.remove()
        if self.subscribe_requests:
            self.add()
        callbacks = self.subscribers[type(event)]
        if not isinstance(event, Tick):
            logging.debug("Processing {event} on {num} callbacks.".format(event=event, num=len(callbacks)))
        for callback in callbacks:
            callback(event)

    def subscribe(self, event_type, callback):
        """
        Subscribe to an event.

        :param event_type: Any hashable object. Intended use is with Event
                           subtypes.
        :param callback: A function that takes a single argument.
        :return: None
        """
        self.subscribe_requests.append((event_type, callback))

    def unsubscribe(self, event_type, callback):
        """
        Unsubscribe from an event.

        :param event_type: The event to unsubscribe from.
        :return: None
        """
        self.unsubscribe_requests.append((event_type, callback))

    def remove(self):
        for r in self.unsubscribe_requests:
            event_type, callback = r
            try:
                self.subscribers[event_type].remove(callback)
            except KeyError:
                pass
            if self.dispatcher and not self.subscribers[event_type]:
                self.dispatcher.unsubscribe(event_type, self.publish)
        self.unsubscribe_requests = []

    def add(self):
        for r in self.subscribe_requests:
            event_type, callback = r
            self.subscribers[event_type].add(callback)
            if self.dispatcher:
                self.dispatcher.subscribe(event_type, self.publish)
        self.subscribe_requests = []


class Queue(object):
    """First in first out array"""

    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def push(self, obj):
        """
        Add an item to the queue.

        :param obj: Any object
        :return: None
        """
        self.in_stack.append(obj)

    def pop(self):
        """
        Retrieve the next item.

        :return: object
        """
        if not self.out_stack:
            self.out_stack = list(reversed(self.in_stack))
            self.in_stack = []
        return self.out_stack.pop()

    def extend(self, _iter):
        self.in_stack.extend(_iter)
