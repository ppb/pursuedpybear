import logging

import ppb.engine as engine
from ppb.event import Collision, Tick, ObjectCreated, ObjectDestroyed
from ppb.components.models import Collider


def check_circle_collision(sprite1, sprite2):
    """
    Check two sprites using circle collision.

    :param sprite1:
    :param sprite2: Sprite must have a pos and radius.
    :return: bool: True if colliding.
    """
    return len(sprite1.pos - sprite2.pos) <= sprite1.radius + sprite2.radius


def colliding(sprite1, sprite2, check=check_circle_collision):
    """
    Check collision between two sprites.

    :param sprite1
    :param sprite2: A sprite must have a pos and attributes needed by the
                    check function.
    :param check: A function that takes two sprites and returns bool
    :return: bool
    """
    return check(sprite1, sprite2)


class Physics(object):
    """Customizable physics engine."""

    def __init__(self, **kwargs):
        if 'collide_function' in kwargs:
            self.collide_function = kwargs['collide_function']
        else:
            self.collide_function = check_circle_collision  # TODO: Cleanup
        self.colliders = set()
        self.commands = []
        self.commands.append((Tick, self.tick))
        self.commands.append((ObjectCreated, self.object_created))
        self.commands.append((ObjectDestroyed, self.object_destroyed))
        engine.message(ObjectCreated(self, self.commands))
        if 'scene' in kwargs:
            scene = kwargs['scene']
            for command in self.commands:
                scene.subscribe(*command)

    def tick(self, _):
        self.check_collisions()

    def check_collisions(self):
        colliders = list(self.colliders)
        while colliders:
            collider = colliders.pop()
            for other in colliders:
                if colliding(collider, other, self.collide_function):
                    engine.message(Collision(collider, other))

    def object_created(self, event):
        if isinstance(event.obj, Collider):
            self.colliders.add(event.obj)

    def game_over(self, _):
        engine.message(ObjectDestroyed(self, self.commands))

    def object_destroyed(self, event):
        if event.obj in self.colliders:
            logging.debug("Colliders before: {}\n{}".format(len(self.colliders),
                                                            self.colliders))
            self.colliders.remove(event.obj)
            logging.debug("Colliders after: {}\n{}".format(len(self.colliders),
                                                           self.colliders))