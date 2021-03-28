"""
"""
import ppb


class Square(ppb.sprites.RectangleSprite):
    width = 1
    height = 4

    image = ppb.Square(0, 0, 255)


class Tall(ppb.sprites.RectangleSprite):
    width = 2
    height = 4

    image = ppb.Image('resources/tall.png')


class Wide(ppb.sprites.RectangleSprite):
    width = 4
    height = 2

    image = ppb.Image('resources/wide.png')


def setup(scene):
    scene.add(Square(position=(0, 0)))
    scene.add(Wide(position=(0, 4)))
    scene.add(Tall(position=(4, 0)))


ppb.run(setup=setup)
