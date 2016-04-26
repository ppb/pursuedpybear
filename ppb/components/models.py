from collections import namedtuple

from ppb import engine
from ppb.event import Tick, ObjectCreated, ObjectDestroyed
from ppb.vmath import Vector2 as Vec

Command = namedtuple("Command", ["event", "callback"])


class Mixable(object):

    def __init__(self, *args, **kwargs):
        pass


class GameObject(Mixable):

    def __init__(self, pos=Vec(0, 0), behaviors=None, *args, **kwargs):
        self.pos = pos
        self.behaviors = []
        if behaviors is not None:
            for event, func in behaviors:
                self.behaviors.append((event, self.bind(func)))
        super(GameObject, self).__init__(pos=pos,
                                         behaviors=behaviors,
                                         *args,
                                         **kwargs)
        engine.message(ObjectCreated(self, self.behaviors))

    def kill(self):
        engine.message(ObjectDestroyed(self, self.behaviors))

    def bind(self, function):
        """
        Bind a callback to Controllable.

        :param function: Must be a function with a signature of
                         function(self, event)
        """

        def callback(event):
            return function(self, event)

        return callback


class Mobile(Mixable):

    def __init__(self, velocity=Vec(0, 0), *args, **kwargs):
        super(Mobile, self).__init__(velocity=velocity,
                                     *args,
                                     **kwargs)
        self.velocity = velocity
        self.behaviors.append((Tick, self.simulate))

    def simulate(self, tick):
        self.pos += self.velocity * tick.sec


class Renderable(Mixable):

    def __init__(self, image=None, image_size=(20, 20), *args, **kwargs):
        super(Renderable, self).__init__(image=image,
                                         image_size=image_size,
                                         *args,
                                         **kwargs)
        self.image = image
        self.image_size = image_size


class HardwarePrimitive(Renderable):

    def __init__(self, color=(255, 255, 255), hardware=None, *args, **kwargs):
        super(HardwarePrimitive, self).__init__(color=color,
                                                hardware=hardware,
                                                *args,
                                                **kwargs)
        self.image = hardware.image_primitive(color, self.image_size)


class Collider(Mixable):

    def __init__(self, radius=0, *args, **kwargs):
        super(Collider, self).__init__(radius=radius, *args, **kwargs)
        self.radius = radius
