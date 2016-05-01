import logging

from ppb import engine
from ppb import hw as hardware
from ppb.utilities import Publisher
from ppb.event import (Quit,
                       Tick,
                       MouseButtonDown,
                       ObjectCreated,
                       ObjectDestroyed,
                       Collision)
from ppb.components import models
from ppb.components.controls import control_move, emit_object
from ppb.physics import Physics
from ppb.vmath import Vector2 as Vector


publisher = Publisher()


class Player(models.GameObject,
             models.Mobile,
             models.HardwarePrimitive,
             models.Collider):
    pass


class Bullet(models.GameObject,
             models.Mobile,
             models.HardwarePrimitive,
             models.Collider):
    pass


class Target(models.GameObject, models.HardwarePrimitive, models.Collider):
    pass


def hit(self, collision):
    is_hit = False
    other = None
    for item in collision.members:
        if item == self:
            is_hit = True
        else:
            other = item
    if is_hit:
        if isinstance(other, Bullet) or isinstance(other, Target):
            self.kill()


def subscribe(event):
    for command in event.commands:
        publisher.subscribe(*command)


def unsubscribe(event):
    for command in event.commands:
        publisher.unsubscribe(*command)


def main():
    logging.basicConfig(level=logging.DEBUG)
    hardware.choose("pygame")
    hardware.init((600, 400), "Targets")
    publisher.subscribe(Quit, hardware.quit)
    publisher.subscribe(ObjectCreated, subscribe)
    publisher.subscribe(ObjectDestroyed, unsubscribe)
    publisher.subscribe(Tick, hardware.update_input)
    hardware.View(publisher,
                  hardware.display(),
                  30,
                  hardware,
                  hardware.image_primitive((0, 0, 0), (600, 400)))
    Physics()

    player_color = (128, 65, 40)
    key_bindings = {"up": ord("w"),
                    "down": ord("s"),
                    "left": ord("a"),
                    "right": ord("d")}
    player_speed = 60
    bullet_params = {"color": (255, 255, 255),
                     "image_size": 4,
                     "hardware": hardware,
                     "behaviors": [(Collision, hit)]}
    controls = [(Tick, control_move(speed=player_speed,
                                    **key_bindings)),
                (MouseButtonDown, emit_object(Bullet, bullet_params, 1, 120))]
    Player(color=player_color,
           hardware=hardware,
           pos=Vector(300, 200),
           behaviors=controls,
           radius=10)
    target_color = (0, 123, 0)
    step = 600 / 6
    for x in range(5):
        Target(color=target_color,
               image_size=20,
               hardware=hardware,
               pos=Vector(step * (x + 1), 50),
               radius=10,
               behaviors=[(Collision, hit)])
    engine.run(publisher)

if __name__ == "__main__":
    main()
