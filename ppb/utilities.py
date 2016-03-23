from __future__ import division

from collections import defaultdict
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
        self.subscribers = defaultdict(dict)
        self.dispatcher = dispatcher

    def publish(self, event):
        """
        Publish an event to subscribers.

        :param event: An Event to publish
        :return: None
        """

        callbacks = self.subscribers[type(event)].values()
        logging.debug("Processing {event} on {num} callbacks.".format(event=event, num=len(callbacks)))
        for callback in callbacks:
            callback(event)

    def subscribe(self, event_type, identity, callback):
        """
        Subscribe to an event.

        :param event_type: Any hashable object. Intended use is with Event subtypes.
        :param identity: A unique hashable identifier of the callback.
        :param callback: A function that takes a single argument.
        :return: None
        """

        self.subscribers[event_type][identity] = callback
        if self.dispatcher:
            self.dispatcher.subscribe(event_type, id(self), self.publish)

    def unsubscribe(self, event_type, identity):
        """
        Unsubscribe from an event.

        :param event_type: The event to unsubscribe from.
        :param identity: a unique hashable identifier
        :return: None
        """

        self.subscribers[event_type].pop(identity, None)
        if self.dispatcher and not self.subscribers[event_type]:
            self.dispatcher.unsubscribe(event_type, id(self))


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
