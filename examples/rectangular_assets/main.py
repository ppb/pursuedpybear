import ppb


tall_rectangle = ppb.Rectangle(200, 0, 0, (1, 2))
wide_rectangle = ppb.Rectangle(100, 200, 0, (2, 1))
square = ppb.Square(200, 200, 100)
tall_triangle = ppb.Triangle(0, 200, 0, (1, 2))
wide_triangle = ppb.Triangle(0, 200, 100, (2, 1))
square_triangle = ppb.Triangle(50, 200, 150)
tall_ellipse = ppb.Ellipse(0, 0, 200, (1, 2))
wide_ellipse = ppb.Ellipse(100, 0, 200, (2, 1))
circle = ppb.Circle(150, 50, 200)


def setup(scene):
    scene.background_color = (0, 0, 0)
    scene.add(ppb.RectangleSprite(width=0.5, height=1, image=tall_rectangle, position=(-2, 2)))
    scene.add(ppb.RectangleSprite(width=1, height=0.5, image=wide_rectangle, position=(0, 2)))
    scene.add(ppb.Sprite(size=1, image=square, position=(2, 2)))
    scene.add(ppb.RectangleSprite(width=0.5, height=1, image=tall_triangle, position=(-2, 0)))
    scene.add(ppb.RectangleSprite(width=1, height=0.5, image=wide_triangle, position=(0, 0)))
    scene.add(ppb.Sprite(image=square_triangle, position=(2, 0)))
    scene.add(ppb.RectangleSprite(width=0.5, height=1, image=tall_ellipse, position=(-2, -2)))
    scene.add(ppb.RectangleSprite(width=1, height=0.5, image=wide_ellipse, position=(0, -2)))
    scene.add(ppb.Sprite(image=circle, position=(2, -2)))


ppb.run(setup)
