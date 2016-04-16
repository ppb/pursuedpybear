import logging

import pygame
from pygame.surface import Surface

from ppb import engine
from ppb.ext import hw_pygame as hardware
from ppb.utilities import Publisher
from ppb.event import Start, Quit, Tick, MouseButtonDown, ObjectCreated, ObjectDestroyed, Collision
from ppb.components import Controller, models
from ppb.components.controls import control_move, emit_object
from ppb.physics import Physics
from ppb.vmath import Vector2 as Vector


publisher = Publisher()


class Player(models.GameObject, models.Mobile, models.Renderable, models.Collider):
    pass


class Bullet(models.GameObject, models.Mobile, models.Renderable, models.Collider):
    pass


class Target(models.GameObject, models.Renderable, models.Collider):
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


def main(_):
    hardware.init((600, 400), "Zombies!")

    publisher.subscribe(Quit, hardware.quit)
    publisher.subscribe(ObjectCreated, subscribe)
    publisher.subscribe(ObjectDestroyed, unsubscribe)
    controller = Controller(publisher, hardware)
    view = hardware.View(publisher, hardware.display, 30, hardware, Surface((600, 400)))
    Physics()

    image = pygame.Surface((20, 20))
    image.fill((128, 65, 40))
    controls = {"up": pygame.K_w,
                "down": pygame.K_s,
                "left": pygame.K_a,
                "right": pygame.K_d,
                "speed": 60}
    sprite_image = pygame.Surface((4, 4))
    sprite_image.fill((255, 255, 255))
    bullet_params = {"image": sprite_image,
                     "image_size": 4,
                     "hardware": hardware,
                     "view": view,
                     "behaviors": [(Collision, hit)]}
    controls = [(Tick, control_move(controller, **controls)),
                (MouseButtonDown, emit_object(Bullet, bullet_params, 1, 120))]
    Player(view=view,
           image=image,
           image_size=20,
           hardware=hardware,
           pos=Vector(300, 200),
           behaviors=controls,
           radius=10)
    target_image = pygame.Surface((20, 20))
    target_image.fill((0, 255, 0))
    step = 600 / 6
    for x in range(5):
        Target(view=view,
               image=target_image,
               image_size=20,
               hardware=hardware,
               pos=Vector(step * (x + 1), 50),
               radius=10,
               behaviors=[(Collision, hit)])

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    publisher.subscribe(Start, main)
    engine.run(publisher)
