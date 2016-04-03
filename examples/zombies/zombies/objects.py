"""
Currently a hack space to build generic objects for game development.

Name not final.
"""

import logging

from ppb import engine
from ppb.event import Tick, Message
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

    def __init__(self, pos, scene, controller, controls, image, view, particle_image):

        super(Player, self).__init__(pos=pos, scene=scene,
                                     image=image, view=view)
        self.life = 10
        self.speed = 100
        self.controller = controller
        self.emitter = Emitter(Particle, particle_image, self.pos, self.scene, self.view)
        self.up = controls.get("up")
        self.down = controls.get("down")
        self.left = controls.get("left")
        self.right = controls.get("right")
        self.fire = controls.get("fire")

    def tick(self, event):
        up = self.controller[self.up[0]][self.up[1]]
        down = self.controller[self.down[0]][self.down[1]]
        left = self.controller[self.left[0]][self.left[1]]
        right = self.controller[self.right[0]][self.right[1]]
        direction = Vector(right - left, down - up).normalize()

        if self.controller[self.fire[0]][self.fire[1]]:
            engine.message(Message(self,
                                   self.emitter,
                                   {'command': "activate",
                                    'target': self.controller.mouse['pos']}))
        self.velocity = direction * self.speed
        super(Player, self).tick(event)
        self.emitter.pos = self.pos


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

    def __init__(self, particle, image, pos, scene, view, **kwargs):
        self.active = False
        self.particle = particle
        self.pos = Vector(*pos)
        self.scene = scene
        self.scene.subscribe(Tick, self.tick)
        self.scene.subscribe(Message, self.activate)
        self.particle_image = image
        self.view = view
        self.run_length = float(kwargs.get("run_time", 0.0))
        self.run_time = self.run_length
        self.interval = float(kwargs.get('interval', 0.001))
        self.interval_count = self.interval
        self.target = Vector(0, 0)
        self.speed = kwargs.get('particle_speed', 60)

    def activate(self, message):
        if message.receiver == self and message.payload['command'] == "activate":
            self.active = True
            self.target = message.payload['target']

    def tick(self, tick):
        if self.active:
            self.run_time += -1 * tick.sec
            if self.run_time <= 0.0:
                self.active = False
                self.run_time = self.run_length
            self.interval_count += -1 * tick.sec
            if self.interval_count <= 0:
                self.emit()
                self.interval_count += self.interval
            self.emit()

    def particle_velocity(self, *args, **kwargs):
        """
        Overwrite in subclass to determine behavior of emitter.

        :param args:
        :param kwargs:
        :return:
        """

        return (self.target - self.pos).normalize() * self.speed

    def emit(self):
        self.particle(self.pos, self.scene, image=self.particle_image,
                      view=self.view, velocity=self.particle_velocity(),
                      life_time=3.0)