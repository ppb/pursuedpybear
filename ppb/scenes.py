from collections import defaultdict
from itertools import chain
from typing import Any
from typing import Iterable
from typing import Iterator

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
        self.kinds = defaultdict(set)
        self.tags = defaultdict(set)

    def __contains__(self, item):
        return item in self.all

    def add(self, game_object: Any, tags: Iterable=()):
        self.all.add(game_object)
        self.kinds[type(game_object)].add(game_object)
        for tag in tags:
            self.tags[tag].add(game_object)

    def get(self, *, kind=None, tag=None) -> Iterator:
        if kind is None and tag is None:
            raise TypeError("get() takes at least one keyword-only argument. 'kind' or 'tag'.")
        kinds = self.kinds[kind] or self.all
        tags = self.tags[tag] or self.all
        return (x for x in kinds.intersection(tags))
