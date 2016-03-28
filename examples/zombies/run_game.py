import logging

import pygame

from ppb import engine
from ppb.controller import Controller
from ppb.ext import hw_pygame as hardware
from ppb.utilities import Publisher
from ppb.event import Quit


def main():
    pygame.init()
    logging.basicConfig(level=logging.DEBUG)
    hardware.init((600, 400))
    scene = Publisher()
    scene.subscribe(Quit, hardware.quit)
    controller = Controller(scene, hardware)
    view = hardware.View(scene, hardware.display, 60, hardware)
    engine.run(scene)

if __name__ == "__main__":
    main()
