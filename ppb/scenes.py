from collections import defaultdict
from itertools import chain

from ppb.abc import Scene
from pygame import MOUSEBUTTONUP, QUIT
from pygame.sprite import LayeredDirty


class BaseScene(Scene):

    def __init__(self, engine, **kwargs):
        """
        Initialize a BaseScene

        :param engine: The containing engine
        :keyword kwargs:
            * *background_color* -- RGB Tuple specifying the background color for the scene
        """
        super().__init__(engine)
        self.background_color = kwargs.get('background_color', (0, 0, 55))
        engine.display.fill(self.background_color)
        self.background = engine.display.copy()
        self.groups = defaultdict(LayeredDirty)
        self.callback_map = {
            QUIT: self.__quit__,
            MOUSEBUTTONUP: self.__mouse_up__
        }

    def render(self):
        """
        Renders all the objects in the groups

        :return: Iterable representing all the drawn rectangles
        """
        window = self.engine.display
        rects = [g.draw(window, self.background) for g in self.groups.values()]
        return chain(*rects)

    def handle_event(self, event):
        """
        Calls the specified callback function from the callback map

        :param event: The event that is supposed to be handled
        """
        self.callback_map.get(event.type, self.__null__)(event)

    def publish_event(self, event):
        pass

    def simulate(self, time_delta: float):
        """
        Update all objects in the group calling their update function

        :param time_delta: Time in seconds that has passed since the last update
        """
        for group in self.groups.values():
            group.update(time_delta)

    def change(self):
        """
        Default case, override in subclass as necessary.

        :return: Tuple specifying if the scene is running and what the scene class is
        """
        return self.running, {"scene_class": self.next}

    def __null__(self, event):
        """
        Do nothing

        :param event: unused
        """
        pass

    def __quit__(self, event):
        """
        Sets running to False and quit to True 

        :param event: unused
        """
        _ = event
        self.running = False
        self.quit = True

    def __mouse_up__(self, event):
        """
        Do nothing

        :param event: unused
        """
        pass
