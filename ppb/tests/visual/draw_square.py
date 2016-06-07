"""
Drawing visual test module.

Depends on functions tested in window.py

Before loop:
    Instantiate a View
    Instantiate a PrimitiveRenderable which expects a color tuple and size.

During Loop:
    Color of primitive should change randomly every 0.5 seconds.
"""
from random import randint

from ppb.tests.visual import Runner
from ppb.components.models import GameObject, Renderable


def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


class FlashingSquare(GameObject, Renderable):

    def __init__(self, *args, **kwargs):
        kwargs["color"] = random_color()
        self.timer = .5

    def tick(self, tick_event):
        self.timer -= tick_event.sec
        if self.timer <= 0:
            self.timer = .5

runner = Runner("pygame")
