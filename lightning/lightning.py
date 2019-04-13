import ppb


class Ship(ppb.BaseSprite):

    def on_update(self, update, signal):
        self.position += ppb.Vector(0, -1).scale(update.time_delta * 4)


def setup(scene):
    scene.add(Ship())


ppb.run(setup=setup)
