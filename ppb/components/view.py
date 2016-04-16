from ppb.event import Tick, Quit, ObjectDestroyed, ObjectCreated
from ppb.vmath import Vector2 as Vector
from ppb.components.models import Renderable
from ppb import engine


class View(object):

    def __init__(self, scene, display, fps, hardware):
        self.render_wait = 1 / fps
        self.countdown = self.render_wait
        self.behaviors = ((Tick, self.tick),
                          (Quit, self.quit),
                          (ObjectDestroyed, self.object_destroyed),
                          (ObjectCreated, self.object_created))
        self.display = display
        self.layers = [set()]
        self.hw = hardware
        self.fps = [[]]
        engine.message(ObjectCreated(self, self.behaviors))

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
        try:
            print("FPS: {}".format(1 / (sum(self.fps[-1]) / len(self.fps[-1]))))
        except ZeroDivisionError:
            print("FPS: N/A")

    def object_destroyed(self, obj):
        self.remove(obj.obj)
        for sprite in self.sprites:
            sprite.object_destroyed(obj)

    def object_created(self, obj):
        obj = obj.obj
        if isinstance(obj, Renderable):
            self.add(Sprite(obj))

    @property
    def sprites(self):
        sprites = []
        for layer in self.layers:
            sprites.extend(list(layer))
        return sprites


class Sprite(object):

    def __init__(self, model):
        self.image = model.image
        self.size = model.image_size
        self.pos = Vector(0, 0)
        self.model = model

    def update(self):
        self.pos = Vector(self.model.pos.x - self.size,
                          self.model.pos.y - self.size)

    def object_destroyed(self, event):
        if event.obj == self.model:
            self.kill()

    def kill(self):
        engine.message(ObjectDestroyed(self, []))
