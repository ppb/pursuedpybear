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
    controls = {"up": pygame.K_w,
                "down": pygame.K_s,
                "left": pygame.K_a,
                "right": pygame.K_d}
    player = zombies.objects.Player((300, 200), scene, controller, controls, image, view)
    image = pygame.Surface((4, 4))
    image.fill((255, 255, 255))
    zombies.objects.Emitter(zombies.objects.Particle, image, (0, 0), scene, view)
    # scene.subscribe(Tick, raise_quit)
    engine.run(scene)

def raise_quit(_):
    engine.message(Quit())

if __name__ == "__main__":
    main()
