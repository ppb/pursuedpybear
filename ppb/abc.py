from typing import Iterable
from typing import Tuple
from typing import Type


class Engine(object):

    def __init__(self):
        self.mouse = {"x": 0, "y": 0, 1: 0, 2: 0, 3: 0}  # type: dict
        # Consider making mouse an object.
        self.keys = []
        self.display = None

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class GameObject(object):

    @property
    def rect(self) -> 'Rectangle':
        raise NotImplementedError

    @property
    def image(self):
        raise NotImplementedError

    @property
    def scene(self) -> 'Scene':
        raise NotImplementedError


class Rectangle(object):
    pass


class Scene(object):

    def __init__(self, engine: Engine):
        # Handle to parent
        self.engine = engine  # type: Engine

        # State
        self.running = True  # type: bool
        self.next = None  # type: Type
        self.groups = None  # type: dict

    def render(self) -> Iterable:
        raise NotImplementedError

    def simulate(self, time_delta: float):
        raise NotImplementedError

    def create_object(self, game_object, *args, **kwargs):
        game_object(self, *args, **kwargs)  # This shouldn't be in the ABC.

    def change(self) -> Tuple[bool, dict]:
        raise NotImplementedError
