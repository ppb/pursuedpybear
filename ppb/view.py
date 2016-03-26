from ppb.event import Tick
from ppb.vmath import Vector2 as Vector


class View(object):

    def __init__(self, scene, display, fps, hardware):
        self.render_wait = 1 / fps
        self.countdown = self.render_wait
        scene.subscribe(Tick, self.tick)
        self.display = display
        self.layers = [[]]
        self.hw = hardware

    def render(self):
        for layer in self.layers:
            for sprite in layer:
                sprite.update()
            self.hw.render(layer)

    def tick(self, event):
        self.countdown += -1 * event.sec
        if self.countdown <= 0:
            self.render()


class Sprite(object):

    def __init__(self, image, size, model):
        self.image = image
        self.size = size
        self.pos = Vector(0, 0)
        self.model = model

    def update(self):
        self.pos = Vector(self.model.pos.x - self.size, self.model.pos.y - self.size)
