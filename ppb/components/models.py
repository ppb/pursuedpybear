from collections import namedtuple

from ppb import engine
from ppb.event import Tick, Message, ObjectCreated, ObjectDestroyed
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

    def __init__(self, image=None, view=None, image_size=0, hardware=None, *args, **kwargs):
        super(Renderable, self).__init__(image=image,
                                         view=view,
                                         image_size=image_size,
                                         *args,
                                         **kwargs)

        view.add(hardware.Sprite(image, self, size=image_size))

    def kill(self):
        super(Renderable, self).kill()
        engine.message(Message(self, None, {"command": "kill"}))


class Collider(Mixable):

    def __init__(self, radius=0, *args, **kwargs):
        super(Collider, self).__init__(radius=radius, *args, **kwargs)
        self.radius = radius
