from collections import defaultdict
from collections.abc import Collection
from typing import Hashable
from typing import Iterable
from typing import Iterator
from typing import Type

from pygame.sprite import LayeredDirty

from ppb.abc import Scene


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

    def __len__(self):
        return len(self.all)

    def add(self, game_object: Hashable, tags: Iterable[Hashable]=()) -> None:
        """
        Add a game_object to the container.

        game_object: Any Hashable object. The item to be added.
        tags: An iterable of Hashable objects. Values that can be used to
              retrieve a group containing the game_object.

        Examples:
            container.add(MyObject())

            container.add(MyObject(), tags=("red", "blue")
        """
        self.all.add(game_object)
        self.kinds[type(game_object)].add(game_object)
        for tag in tags:
            self.tags[tag].add(game_object)

    def get(self, *, kind: Type=None, tag: Hashable=None, **_) -> Iterator:
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
        kinds = self.kinds[kind] or self.all
        tags = self.tags[tag] or self.all
        return (x for x in kinds.intersection(tags))

    def remove(self, game_object: Hashable) -> None:
        """
        Remove the given object from the container.

        game_object: A hashable contained by container.

        Example:
            container.remove(myObject)
        """
        self.all.remove(game_object)
        self.kinds[type(game_object)].remove(game_object)
        for s in self.tags.values():
            s.discard(game_object)


class BaseScene(Scene):

    def __init__(self, engine, *, background_color=(0, 0, 100),
                 container_class=GameObjectCollection, set_up=None, **kwargs):
        super().__init__(engine)
        self.background_color = background_color
        self.background = None
        self.game_objects = container_class()
        self.render_group = LayeredDirty()
        if set_up is not None:
            set_up(self)

    def __contains__(self, item: Hashable) -> bool:
        return item in self.game_objects

    def __iter__(self):
        return (x for x in self.game_objects)

    def render(self):
        window = self.engine.display
        self.render_group.add(s for s in self.game_objects)
        return self.render_group.draw(window, self.background)

    def simulate(self, time_delta: float):
        for game_object in self.game_objects:
            game_object.on_update(time_delta)

    def change(self):
        """
        Default case, override in subclass as necessary.
        """
        return self.running, {"scene_class": self.next}

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
