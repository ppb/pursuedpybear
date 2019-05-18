"""
A simple rendition of the three-body problem. Also demonstrates the use of
two-phase updates.

The three body problem comes from astrophysics. Basically, applying the
gravitaional two three celestial bodies produces a problem that does not have a
perfect mathematical solution, and must be solved through simulations.
"""

import logging
from ppb import BaseSprite, make_engine, Vector
from ppb.features.twophase import TwoPhaseMixin, TwoPhaseSystem


class Planet(BaseSprite, TwoPhaseMixin):
    #: A constant to apply to gravity
    G_CONST = 1

    velocity = Vector(0, 0)

    def get_bodies(self, scene):
        for planet in scene.get(kind=Planet):
            yield planet, (planet.position - self.position)

    def on_update(self, event, signal):
        # This assumes all planets have the same mass
        force = sum(
            (
                delta / (len(delta) ** 2)
                for planet, delta in self.get_bodies(event.scene)
            ),
            Vector(0, 0)
        )

        self.velocity += force * self.G_CONST * event.time_delta

        self.stage_changes(
            position=self.position + self.velocity * event.time_delta
        )


def setup(scene):
    scene.add(Planet(position=(3, 0), velocity=Vector(0, 1)))
    scene.add(Planet(position=(-3, 3), velocity=Vector(1, -1)))
    scene.add(Planet(position=(-3, -3), velocity=Vector(-1, 0)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Not good practice, https://github.com/ppb/pursuedpybear/issues/263
    eng = make_engine(setup)
    eng.systems_classes += (TwoPhaseSystem,)
    with eng:
        eng.run()
