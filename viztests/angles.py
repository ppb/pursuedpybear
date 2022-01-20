"""
Tests rotation vs Vector angles

The center sprite should always face the orbiting sprite, and they should be
moving counter-clockwise.
"""
import ppb

ROTATION_RATE = 90


class CenterSprite(ppb.Sprite):
    image = ppb.Image('player.png')

    def on_update(self, event, signal):
        self.rotate(ROTATION_RATE * event.time_delta)


class OrbitSprite(ppb.Sprite):
    position = ppb.Vector(0, -2)
    image = ppb.Image('target.png')

    def on_update(self, event, signal):
        self.position = self.position.rotate(ROTATION_RATE * event.time_delta)


def setup(scene):
    scene.add(CenterSprite())
    scene.add(OrbitSprite())


ppb.run(setup)
