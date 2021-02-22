import ppb


class RaceCar(ppb.RectangleSprite):
    pass


def setup(scene):
    scene.add(RaceCar())


ppb.run(setup=setup)