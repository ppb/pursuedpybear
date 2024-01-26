from typing import Callable

from ppb_core.gomlib import GameObject


class Scene(GameObject):

    def __init__(self, *, set_up: Callable = None, **props):
        super().__init__(**props)

        if set_up is not None:
            set_up(self)
