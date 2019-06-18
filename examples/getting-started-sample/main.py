import ppb
from ppb import keycodes
from ppb.events import KeyPressed, KeyReleased


class Player(ppb.BaseSprite):
    direction = ppb.Vector(0, 0)
    speed = 4
    position = ppb.Vector(0, -3)
    left = keycodes.Left
    right = keycodes.Right
    shoot = keycodes.Space

    def on_update(self, update_event, signal):
        if self.direction.x and self.direction.y:
            direction = self.direction.normalize()
        else:
            direction = self.direction
        self.position += direction * self.speed * update_event.time_delta

    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == self.left:
            self.direction += ppb.Vector(-1, 0)
        elif key_event.key == self.right:
            self.direction += ppb.Vector(1, 0)
        elif key_event.key == self.shoot:
            key_event.scene.add(Projectile(position=self.position + ppb.Vector(0, 0.5)))

    def on_key_released(self, key_event: KeyReleased, signal):
        if key_event.key == self.left:
            self.direction += ppb.Vector(1, 0)
        elif key_event.key == self.right:
            self.direction += ppb.Vector(-1, 0)


class Projectile(ppb.BaseSprite):
    size = 0.25
    direction = ppb.Vector(0, 1)
    speed = 6

    def on_update(self, update_event, signal):
        if self.direction:
            direction = self.direction.normalize()
        else:
            direction = self.direction
        self.position += direction * self.speed * update_event.time_delta


class Target(ppb.BaseSprite):

    def on_update(self, update_event, signal):
        for p in update_event.scene.get(kind=Projectile):
            if (p.position - self.position).length <= self.size:
                update_event.scene.remove(self)
                update_event.scene.remove(p)
                break


def setup(scene):
    scene.add(Player())

    for x in range(-4, 5, 2):
        scene.add(Target(position=ppb.Vector(x, 3)))


ppb.run(setup)
