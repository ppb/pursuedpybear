from collections import defaultdict
from itertools import chain

from ppb.abc import Scene
from pygame import MOUSEBUTTONUP, QUIT
from pygame.sprite import LayeredDirty


class BaseScene(Scene):

    def __init__(self, engine, *, background_color=(0, 0, 55), **kwargs):
        super().__init__(engine)
        self.background_color = background_color
        self.background = engine.display.copy()
        self.background.fill(self.background_color)
        self.groups = defaultdict(LayeredDirty)
        self.render_group = LayeredDirty()

    def render(self):
        window = self.engine.display
        self.render_group.add(chain(g.sprites() for g in self.groups.values()))
        return self.render_group.draw(window, self.background)

    def simulate(self, time_delta: float):
        for group in list(self.groups.values()):
            group.update(self, time_delta)

    def change(self):
        """
        Default case, override in subclass as necessary.
        """
        return self.running, {"scene_class": self.next}

    def add(self, game_object):
        pass


class GameObjectContainer:

    def __init__(self):
        self.all = set()

    def add(self, game_object):
        self.all.add(game_object)

    def __contains__(self, item):
        return item in self.all
