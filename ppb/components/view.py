from ppb.event import Tick, Quit
from ppb.vmath import Vector2 as Vector


class View(object):

    def __init__(self, scene, display, fps, hardware):
        self.render_wait = 1 / fps
        self.countdown = self.render_wait
        scene.subscribe(Tick, self.tick)
        scene.subscribe(Quit, self.quit)
        self.display = display
        self.layers = [set()]
        self.hw = hardware
        self.fps = [[]]

    def render(self):
        for layer in self.layers:
            for sprite in layer:
                sprite.update()
            self.hw.render(layer)
        self.hw.draw_screen()

    def tick(self, event):
        self.calculate_fps(event.sec)
        self.countdown += -1 * event.sec
        if self.countdown <= 0:
            self.render()
            self.countdown += self.render_wait

    def add(self, sprite, layer=0):
        """
        Add a sprite to the view.

        :param sprite: Sprite
        :param layer: Layer to render the sprite at.
        :return: None
        """
        while len(self.layers) < layer + 1:
            self.layers.append(set())
        self.layers[layer].add(sprite)

    def remove(self, sprite):
        """
        Remove a sprite from the view.

        :param sprite: Sprite
        :return: none
        """

        for layer in self.layers:
            try:
                layer.remove(sprite)
            except ValueError:
                pass

    def change_layer(self, sprite, layer):
        self.remove(sprite)
        self.add(sprite, layer)

    def calculate_fps(self, time):
        self.fps[0].append(time)
        for index, rates in enumerate(self.fps):
            if len(rates) == 10:
                average = sum(rates) / 10.0
                try:
                    self.fps[index + 1].append(average)
                except IndexError:
                    self.fps.append([average])

    def quit(self, _):
        print("FPS: {}".format(1 / (sum(self.fps[-1]) / len(self.fps[-1]))))


class Sprite(object):

    def __init__(self, image, model, size=0):
        self.image = image
        self.size = size
        self.pos = Vector(0, 0)
        self.model = model

    def update(self):
        self.pos = Vector(self.model.pos.x - self.size,
                          self.model.pos.y - self.size)
