import logging

import pygame
from pygame.surface import Surface

from ppb import engine, Controller
from ppb.ext import hw_pygame as hardware
from ppb.utilities import Publisher
from ppb.event import Quit, Tick
import zombies.objects


def main():
    pygame.init()
    logging.basicConfig(level=logging.DEBUG)
    hardware.init((600, 400), "Zombies!")

    scene = Publisher()
    scene.subscribe(Quit, hardware.quit)
    controller = Controller(scene, hardware)
    view = hardware.View(scene, hardware.display, 30, hardware, Surface((600, 400)))

    image = pygame.Surface((20, 20))
    image.fill((128, 15, 15))
    controls = {"up": ('key', pygame.K_w),
                "down": ('key', pygame.K_s),
                "left": ('key', pygame.K_a),
                "right": ('key', pygame.K_d),
                "fire": ("mouse", 0)}
    particle_image = pygame.Surface((4, 4))
    particle_image.fill((255, 255, 255))
    zombies.objects.Player((300, 200), scene, controller, controls,
                           image, view, particle_image)
    engine.run(scene)


def raise_quit(_):
    engine.message(Quit())


if __name__ == "__main__":
    main()
