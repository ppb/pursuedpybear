"""
Visual test of the layering system.

The grey circle mover should render above the purple up arrows and below
the yellow down arrows.
"""
from itertools import cycle

import ppb


class Mover(ppb.BaseSprite):
    image = ppb.Image("viztests/resources/mover.png")
    position = ppb.Vector(0, -4)
    velocity = ppb.Vector(0, 3)

    def on_update(self, update: ppb.events.Update, signal):
        self.position += self.velocity * update.time_delta
        if self.position.y > 4 or self.position.y < -4:
            self.velocity *= -1


class TravelOver(ppb.BaseSprite):
    image = ppb.Image("viztests/resources/travel_over.png")
    layer = -1


class TravelUnder(ppb.BaseSprite):
    image = ppb.Image("viztests/resources/travel_under.png")
    layer = 1


def setup(scene):
    scene.add(Mover())
    for x, klass in zip(range(-3, 4), cycle((TravelOver, TravelUnder))):
        scene.add(klass(position=ppb.Vector(0, x)))


ppb.run(setup)
