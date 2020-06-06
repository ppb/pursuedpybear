import ppb

font = ppb.Font("resources/ubuntu_font/Ubuntu-R.ttf", size=72)
my_first_text = ppb.Text("My first text", font=font, color=(255, 255, 255))
my_second_text = ppb.Text("My second text", font=font, color=(255, 255, 255))


def setup(scene):
    scene.add(ppb.Sprite(image=my_first_text))
    scene.add(ppb.Sprite(image=my_second_text, position=ppb.Vector(0, -2)))


ppb.run(setup)
