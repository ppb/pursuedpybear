import ppb


tall_rectangle = ppb.Square(200, 0, 0, (1, 2))
wide_rectangle = ppb.Square(100, 200, 0, (2, 1))
tall_triangle = ppb.Triangle(0, 200, 0, (1, 2))
wide_triangle = ppb.Triangle(0, 200, 100, (2, 1))
tall_ellipse = ppb.Circle(0, 0, 200, (1, 2))
wide_ellipse = ppb.Circle(100, 0, 200, (2, 1))


def setup(scene):
    scene.background_color = (0, 0, 0)
    scene.add(ppb.RectangleSprite(width=0.5, height=1, image=tall_rectangle, position=(-1, 2)))
    scene.add(ppb.RectangleSprite(width=1, height=0.5, image=wide_rectangle, position=(1, 2)))
    scene.add(ppb.RectangleSprite(width=0.5, height=1, image=tall_triangle, position=(-1, 0)))
    scene.add(ppb.RectangleSprite(width=1, height=0.5, image=wide_triangle, position=(1, 0)))
    scene.add(ppb.RectangleSprite(width=0.5, height=1, image=tall_ellipse, position=(-1, -2)))
    scene.add(ppb.RectangleSprite(width=1, height=0.5, image=wide_ellipse, position=(1, -2)))


ppb.run(setup)
