"""
The Game Object Model.
"""
from collections import defaultdict, deque
from collections.abc import Collection
from typing import Hashable
from typing import Iterable
from typing import Iterator
from typing import Type
import warnings

from ppb.errors import BadChildException


class Children(Collection):
    """
    A container for game objects.

    Supports tagging.
    """

    def __init__(self):
        self._all = set()
        self._kinds = defaultdict(set)
        self._tags = defaultdict(set)

    def __contains__(self, item: Hashable) -> bool:
        return item in self._all

    def __iter__(self) -> Iterator[Hashable]:
        return (x for x in list(self._all))

    def __len__(self) -> int:
        return len(self._all)

    def add(self, child: Hashable, tags: Iterable[Hashable] = ()) -> Hashable:
        """
        Add a child.

        :param child: Any Hashable object. The item to be added.
        :param tags: An iterable of Hashable objects. Values that can be used to
              retrieve a group containing the child.

        Examples: ::

            children.add(MyObject())

            children.add(MyObject(), tags=("red", "blue")
        """
        # Ugh, this is copied in EngineChildren
        if isinstance(child, type):
            raise BadChildException(child)

        if isinstance(tags, (str, bytes)):
            raise TypeError("You passed a string instead of an iterable, this probably isn't what you intended.\n\nTry making it a tuple.")

        self._all.add(child)

        for kind in type(child).mro():
            self._kinds[kind].add(child)
        for tag in tags:
            self._tags[tag].add(child)

        return child

    def remove(self, child: Hashable) -> Hashable:
        """
        Remove the given object from the container.

        :param child: A hashable contained by container.

        Example: ::

            container.remove(myObject)
        """
        # Ugh, this is copied in EngineChildren
        self._all.remove(child)
        for kind in type(child).mro():
            self._kinds[kind].remove(child)
        for s in self._tags.values():
            s.discard(child)

        return child

    def get(self, *, kind: Type = None, tag: Hashable = None, **_) -> Iterator:
        """
        Iterate over the objects by kind or tag.

        :param kind: Any type. Pass to get a subset of contained items with the given
              type.
        :param tag: Any Hashable object. Pass to get a subset of contained items with
             the given tag.

        Pass both kind and tag to get objects that are both that type and that
        tag.

        Examples: ::

            children.get(type=MyObject)

            children.get(tag="red")

            children.get(type=MyObject, tag="red")
        """
        if kind is None and tag is None:
            raise TypeError("get() takes at least one keyword-only argument. 'kind' or 'tag'.")
        kinds = self._all
        tags = self._all
        if kind is not None:
            kinds = self._kinds[kind]
        if tag is not None:
            tags = self._tags[tag]
        return (x for x in kinds.intersection(tags))

    def walk(self):
        """
        Iterate over the children and their children.
        """
        for child in self._all:
            yield child
            if hasattr(child, 'children') and hasattr(child.children.walk):
                yield from child.children.walk()

    def tags(self):
        """
        Generates all of the tags currently in the collections
        """
        yield from self._tags

    def kinds(self):
        """
        Generates all types of the children (including super types)
        """
        yield from self._kinds


class GameObject:
    """
    A generic parent class for game objects. Handles:

    * Property-based init (``Sprite(position=pos, image=img)``)
    * Children management
    """
    #: The children of this object
    children: Children

    def __init__(self, **props):
        super().__init__()

        self.children = Children()
        for k, v in props.items():
            setattr(self, k, v)

    def __iter__(self) -> Iterator:
        """
        Shorthand for :meth:`Children.__iter__()`
        """
        yield from self.children

    def add(self, child: Hashable, tags: Iterable = ()) -> None:
        """
        Shorthand for :meth:`Children.add()`
        """
        return self.children.add(child, tags)

    def get(self, *, kind: Type = None, tag: Hashable = None, **kwargs) -> Iterator:
        """
        Shorthand for :meth:`Children.get()`
        """
        return self.children.get(kind=kind, tag=tag, **kwargs)

    def remove(self, child: Hashable) -> None:
        """
        Shorthand for :meth:`Children.remove()`
        """
        return self.children.remove(child)


def walk(root):
    """
    Conducts a walk of the GOM tree from the root.

    Includes the root.

    Is non-recursive.
    """
    q = deque([root])
    while q:
        cur = q.popleft()
        yield cur
        if hasattr(cur, 'children'):
            q.extend(cur.children)
