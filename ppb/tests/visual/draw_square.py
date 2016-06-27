"""
Drawing visual test module.

Depends on functions tested in window.py

Before loop:
    Instantiate a View
    Instantiate a PrimitiveRenderable which expects a color tuple and size.
"""
from random import randint

from ppb.tests.visual import Runner
from ppb.components.models import GameObject, Renderable


def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


class Square(GameObject, Renderable):

    def __init__(self, *args, **kwargs):
        kwargs["color"] = random_color()


runner = Runner("sdl2")
square = Square()
runner.run()
