from ppb.event import Tick
from ppb.view import Sprite
from ppb.vmath import Vector2 as Vector


class Mob(object):

    def __init__(self, pos, scene, velocity=(0, 0), *args, **kwargs):
        _ = args
        _ = kwargs
        self.pos = Vector(*pos)
        self.velocity = Vector(*velocity)
        scene.subscribe(Tick, self.tick)

    def tick(self, event):
        self.pos += self.velocity * event.sec


class Renderable(object):

    def __init__(self, image, size, *args, **kwargs):
        _ = args
        _ = kwargs
        self.sprite = Sprite(image, size, self)

    def remove(self):
        self.sprite.remove()
        self.sprite = None


class Zombie(Mob, Renderable):

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


class Player(Mob, Renderable):

    size = 1

    def __init__(self, pos, scene, controller, controls, image, velocity=(0, 0)):
        super(Player, self).__init__(pos=pos, scene=scene, velocity=velocity, image=image, size=self.size)
        self.life = 10
        self.speed = 1
        self.controller = controller
        self.up = controls["up"]
        self.down = controls["down"]
        self.left = controls["left"]
        self.right = controls["right"]

    def tick(self, event):
        direction = Vector(self.controller.keys[self.down] - self.controller.keys[self.up],
                           self.controller.keys[self.right] - self.controller.keys[self.left]).normalize()
        self.velocity = direction * self.speed
        super(Player, self).tick(event)
