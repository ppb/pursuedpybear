import logging

from ppb.event import Tick
from ppb.ext.hw_pygame import Sprite
from ppb.vmath import Vector2 as Vector


class Mob(object):

    def __init__(self, pos, scene, velocity=(0, 0), *args, **kwargs):
        self.pos = Vector(*pos)
        self.velocity = Vector(*velocity)
        logging.debug("Mob initialized.")
        scene.subscribe(Tick, self.tick)

    def tick(self, event):
        self.pos += self.velocity * event.sec


class Renderable(Mob):

    def __init__(self, pos, scene, velocity=(0, 0), image=None, view=None, *args, **kwargs):
        super(Renderable, self).__init__(pos, scene, velocity, image, view, *args, **kwargs)
        self.sprite = Sprite(image, self)
        self.view = view
        view.add(self.sprite)

    def remove(self):
        self.view.remove()
        self.sprite = None


class Zombie(Renderable):

    size = 1
    acceleration = 1
    max_speed = 2

    def __init__(self, pos, scene, image, velocity=(0, 0)):
        super(Zombie, self).__init__(pos=pos, scene=scene, velocity=velocity, image=image, size=self.size)
        self.target = Vector(0, 0)

    def tick(self, event):
        self.velocity += self.target - self.pos * self.acceleration * event.sec
        self.velocity.truncate(self.max_speed)
        super(Zombie, self).tick(event)


class Player(Renderable):

    size = 1

    def __init__(self, pos, scene, controller, controls, image, view):

        super(Player, self).__init__(pos, scene, (0, 0), image, view)
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
