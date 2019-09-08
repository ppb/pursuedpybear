"""
Tests primitive asset types: Square, Circle, and Triangle.

Should display a red square in the bottom left, a black triangle up, and a
magenta circle bottom right.
"""
import ppb


class Rotating(ppb.Sprite):
    """
    A rotating sprite.
    """
    degrees_per_second = 90

    def on_update(self, event: ppb.events.Update, signal):
        self.rotation += event.time_delta * self.degrees_per_second


class Square(Rotating):
    image = ppb.Square(255, 50, 75)


class Triangle(Rotating):
    image = ppb.Triangle(0, 0, 0)


class Circle(Rotating):
    image = ppb.Circle(255, 71, 182)


def setup(scene):
    scene.background_color = (160, 155, 180)
    scene.add(Square(position=ppb.Vector(-2, 0)))
    scene.add(Triangle(position=ppb.Vector(0, 2)))
    scene.add(Circle(position=ppb.Vector(2, 0)))


ppb.run(setup=setup)
