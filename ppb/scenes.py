from collections import defaultdict
from collections.abc import Collection
from numbers import Number
from typing import Callable
from typing import Hashable
from typing import Iterable
from typing import Iterator
from typing import Sequence
from typing import Type

from ppb.camera import Camera
from ppb.events import EventMixin


class GameObjectCollection(Collection):
    """A container for game objects."""

    def __init__(self):
        self.all = set()
        self.kinds = defaultdict(set)
        self.tags = defaultdict(set)

    def __contains__(self, item: Hashable) -> bool:
        return item in self.all

    def __iter__(self) -> Iterator[Hashable]:
        return (x for x in list(self.all))

    def __len__(self) -> int:
        return len(self.all)

    def add(self, game_object: Hashable, tags: Iterable[Hashable] = ()) -> None:
        """
        Add a game_object to the container.

        game_object: Any Hashable object. The item to be added.
        tags: An iterable of Hashable objects. Values that can be used to
              retrieve a group containing the game_object.

        Examples:
            container.add(MyObject())

            container.add(MyObject(), tags=("red", "blue")
        """
        if isinstance(tags, (str, bytes)):
            raise TypeError("You passed a string instead of an iterable, this probably isn't what you intended.\n\nTry making it a tuple.")
        self.all.add(game_object)

        for kind in type(game_object).mro():
            self.kinds[kind].add(game_object)
        for tag in tags:
            self.tags[tag].add(game_object)

    def get(self, *, kind: Type = None, tag: Hashable = None, **_) -> Iterator:
        """
        Get an iterator of objects by kind or tag.

        kind: Any type. Pass to get a subset of contained items with the given
              type.
        tag: Any Hashable object. Pass to get a subset of contained items with
             the given tag.

        Pass both kind and tag to get objects that are both that type and that
        tag.

        Examples:
            container.get(type=MyObject)

            container.get(tag="red")

            container.get(type=MyObject, tag="red")
        """
        if kind is None and tag is None:
            raise TypeError("get() takes at least one keyword-only argument. 'kind' or 'tag'.")
        kinds = self.all
        tags = self.all
        if kind is not None:
            kinds = self.kinds[kind]
        if tag is not None:
            tags = self.tags[tag]
        return (x for x in kinds.intersection(tags))

    def remove(self, game_object: Hashable) -> None:
        """
        Remove the given object from the container.

        game_object: A hashable contained by container.

        Example:
            container.remove(myObject)
        """
        self.all.remove(game_object)
        for kind in type(game_object).mro():
            self.kinds[kind].remove(game_object)
        for s in self.tags.values():
            s.discard(game_object)


class BaseScene(EventMixin):
    # Background color, in RGB, each channel is 0-255
    background_color: Sequence[int] = (0, 0, 100)
    container_class: Type = GameObjectCollection

    def __init__(self, *,
                 set_up: Callable = None, pixel_ratio: Number = 64,
                 **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.game_objects = self.container_class()
        self.main_camera = Camera(pixel_ratio=pixel_ratio)

        if set_up is not None:
            set_up(self)

    def __contains__(self, item: Hashable) -> bool:
        return item in self.game_objects

    def __iter__(self) -> Iterator:
        return (x for x in self.game_objects)

    @property
    def kinds(self):
        return self.game_objects.kinds

    @property
    def tags(self):
        return self.game_objects.tags

    @property
    def main_camera(self) -> Camera:
        return next(self.game_objects.get(tag="main_camera"))

    @main_camera.setter
    def main_camera(self, value: Camera):
        for camera in self.game_objects.get(tag="main_camera"):
            self.game_objects.remove(camera)
        self.game_objects.add(value, tags=["main_camera"])

    def add(self, game_object: Hashable, tags: Iterable=())-> None:
        """
        Add a game_object to the scene.

        game_object: Any GameObject object. The item to be added.
        tags: An iterable of Hashable objects. Values that can be used to
              retrieve a group containing the game_object.

        Examples:
            scene.add(MyGameObject())

            scene.add(MyGameObject(), tags=("red", "blue")
        """
        self.game_objects.add(game_object, tags)

    def get(self, *, kind: Type=None, tag: Hashable=None, **kwargs) -> Iterator:
        """
        Get an iterator of GameObjects by kind or tag.

        kind: Any type. Pass to get a subset of contained GameObjects with the
              given type.
        tag: Any Hashable object. Pass to get a subset of contained GameObjects
             with the given tag.

        Pass both kind and tag to get objects that are both that type and that
        tag.

        Examples:
            scene.get(type=MyGameObject)

            scene.get(tag="red")

            scene.get(type=MyGameObject, tag="red")
        """
        return self.game_objects.get(kind=kind, tag=tag, **kwargs)

    def remove(self, game_object: Hashable) -> None:
        """
        Remove the given object from the scene.

        game_object: A game object.

        Example:
            scene.remove(my_game_object)
        """
        self.game_objects.remove(game_object)
