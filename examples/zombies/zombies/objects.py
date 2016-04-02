"""
Currently a hack space to build generic objects for game development.

Name not final.
"""

import logging

from ppb.event import Tick, MouseButtonDown
from ppb.ext.hw_pygame import Sprite
from ppb.vmath import Vector2 as Vector


class Mob(object):

    def __init__(self, pos, scene, velocity=(0, 0), *args, **kwargs):
        self.pos = Vector(*pos)
        self.velocity = Vector(*velocity)
        self.scene = scene
        scene.subscribe(Tick, self.tick)

    def tick(self, event):
        self.pos += self.velocity * event.sec

    def kill(self):
        self.scene.unsubscribe(Tick, self.tick)


class Renderable(Mob):

    def __init__(self, pos, scene, image=None, view=None, *args, **kwargs):
        super(Renderable, self).__init__(pos=pos, scene=scene, image=image,
                                         view=view, *args, **kwargs)
        self.sprite = Sprite(image, self)
        self.view = view
        view.add(self.sprite)

    def kill(self):
        super(Renderable, self).kill()
        self.sprite.kill()
        self.sprite = None


class Zombie(Renderable):

    size = 1
    acceleration = 1
    max_speed = 2

    def __init__(self, pos, scene, image):
        super(Zombie, self).__init__(pos=pos, scene=scene, image=image, size=self.size)
        self.target = Vector(0, 0)

    def tick(self, event):
        self.velocity += self.target - self.pos * self.acceleration * event.sec
        self.velocity.truncate(self.max_speed)
        super(Zombie, self).tick(event)


class Player(Renderable):

    size = 1

    def __init__(self, pos, scene, controller, controls, image, view):

        super(Player, self).__init__(pos=pos, scene=scene,
                                     image=image, view=view)
        self.life = 10
        self.speed = 100
        self.controller = controller
        self.up = controls["up"]
        self.down = controls["down"]
        self.left = controls["left"]
        self.right = controls["right"]

    def tick(self, event):
        logging.debug(self.controller.mouse)
        direction = Vector(self.controller.key(self.right) - self.controller.key(self.left),
                           self.controller.key(self.down) - self.controller.key(self.up)).normalize()
        self.velocity = direction * self.speed
        super(Player, self).tick(event)


class Particle(Renderable):
    """
    A Particle Base Class
    """

    def __init__(self, pos, scene, image=None, view=None, *args, **kwargs):
        """

        :param pos:
        :param scene:
        :param image:
        :param view:
        :param args:
        :param kwargs: velocity: used by base classes
                                 good for fixed speed and direction
                                 particles.
                       life_time: Amount of time to persist
        :return:
        """
        super(Particle, self).__init__(pos=pos, scene=scene,
                                       image=image, view=view, *args, **kwargs)
        self.life_time = kwargs.get('life_time', float('inf'))

    def tick(self, event):
        self.life_time += -1 * event.sec
        if self.life_time <= 0.0:
            self.kill()
        super(Particle, self).tick(event)


class Emitter(object):

    def __init__(self, particle, image, pos, scene, view):
        self.active = False
        self.particle = particle
        self.pos = Vector(*pos)
        self.scene = scene
        self.scene.subscribe(Tick, self.tick)
        self.scene.subscribe(MouseButtonDown, self.emit)
        self.particle_image = image
        self.view = view

    def emit(self, _):
        self.active = True

    def tick(self, tick):
        if self.active:
            self.particle(self.pos, self.scene, image=self.particle_image,
                          view=self.view, velocity=self.particle_velocity())

    def particle_velocity(self):
        return Vector(60, 60)