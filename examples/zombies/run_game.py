import logging

import pygame
from pygame.surface import Surface

from ppb import engine
from ppb.ext import hw_pygame as hardware
from ppb.utilities import Publisher
from ppb.event import Quit, Tick
from ppb.components import Controller, models
from ppb.components.controls import control_move
from ppb.vmath import Vector2 as Vector


class Player(models.Controllable, models.Renderable):
    pass


def main():
    logging.basicConfig(level=logging.DEBUG)
    hardware.init((600, 400), "Zombies!")

    scene = Publisher()
    scene.subscribe(Quit, hardware.quit)
    controller = Controller(scene, hardware)
    view = hardware.View(scene, hardware.display, 30, hardware, Surface((600, 400)))

    image = pygame.Surface((20, 20))
    image.fill((128, 15, 15))
    controls = {"up": pygame.K_w,
                "down": pygame.K_s,
                "left": pygame.K_a,
                "right": pygame.K_d,
                "speed": 60}
    controls = [(Tick, control_move(controller, **controls))]
    Player(scene=scene,
           view=view,
           image=image,
           image_size=20,
           hardware=hardware,
           pos=Vector(300, 200),
           commands=controls)
    engine.run(scene)


if __name__ == "__main__":
    main()
