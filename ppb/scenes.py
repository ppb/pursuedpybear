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
        self.callback_map = {
            QUIT: self.__quit__,
            MOUSEBUTTONUP: self.__mouse_up__
        }

    def render(self):
        window = self.engine.display
        self.render_group.add(chain(g.sprites() for g in self.groups.values()))
        return self.render_group.draw(window, self.background)

    def handle_event(self, event):
        self.callback_map.get(event.type, self.__null__)(event)

    def publish_event(self, event):
        pass

    def simulate(self, time_delta: float):
        for group in list(self.groups.values()):
            group.update(time_delta)

    def change(self):
        """
        Default case, override in subclass as necessary.
        """
        return self.running, {"scene_class": self.next}

    def __null__(self, event):
        pass

    def __quit__(self, event):
        _ = event
        self.running = False
        self.quit = True

    def __mouse_up__(self, event):
        pass
