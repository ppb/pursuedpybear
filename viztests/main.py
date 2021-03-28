"""
An array of sprites using different aspect ratios in various colors on a black background.

Order:

______________________________________________________________
|    shape  || tall         | wide         | square          |
--------------------------------------------------------------
| rectangle || tall_rect    | wide_rect    | square          |
| triangle  || tall_tri     | wide_tri     | equilateral_tri |
| ellipse   || tall_ellipse | wide_ellipse | circle          |
______________________________________________________________
"""

import ppb


def setup(scene):
    scene.background_color = (0, 0, 0)
    scene.add(ppb.RectangleSprite(
        width=0.5, height=1,
        image=ppb.Rectangle(200, 0, 0, (1, 2)), position=(-2, 2)))
    scene.add(ppb.RectangleSprite(
        width=1, height=0.5,
        image=ppb.Rectangle(100, 200, 0, (2, 1)), position=(0, 2)))
    scene.add(ppb.Sprite(size=1,
                         image=ppb.Square(200, 200, 100), position=(2, 2)))
    scene.add(ppb.RectangleSprite(
        width=0.5, height=1,
        image=ppb.Triangle(0, 200, 0, (1, 2)), position=(-2, 0)))
    scene.add(ppb.RectangleSprite(
        width=1, height=0.5,
        image=ppb.Triangle(0, 200, 100, (2, 1)), position=(0, 0)))
    scene.add(ppb.Sprite(image=ppb.Triangle(50, 200, 150), position=(2, 0)))
    scene.add(ppb.RectangleSprite(
        width=0.5, height=1,
        image=ppb.Ellipse(0, 0, 200, (1, 2)), position=(-2, -2)))
    scene.add(ppb.RectangleSprite(
        width=1, height=0.5,
        image=ppb.Ellipse(100, 0, 200, (2, 1)), position=(0, -2)))
    scene.add(ppb.Sprite(image=ppb.Circle(150, 50, 200), position=(2, -2)))


ppb.run(setup)
