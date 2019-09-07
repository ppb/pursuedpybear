"""
Tests that sprites drawn with the square primitive default rotate correctly.

Verify that the square rotates and doesn't resize.
"""
import ppb


class Square(ppb.Sprite):
    degrees_per_second = 180

    def on_update(self, update: ppb.events.Update, signal):
        self.rotation += self.degrees_per_second * update.time_delta


def setup(scene):
    scene.add(Square())


ppb.run(setup=setup)
