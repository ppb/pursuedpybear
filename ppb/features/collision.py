"""
A collision subsystem with various colliders available.
"""
from itertools import combinations

from ppb.sprites import Sprite
from ppb.systemslib import System


class CollidedWithMixin:
    """
    Provides a mechanism for CollisionCheckerSystem to inform sprites when
    they collide with something.

    This is a mixin added to CanCollideCircleMixin and
    CanCollideSquareMixin. You do not need to to add it to your sprites if
    you are using one of them.
    """

    def on_collided_with(self, other):
        """
        Another sprite has collided with this sprite.

        This is meant to be overridden in your sprites. If a sprite has a
        collider mixin, but doesn't respond to those collisions, you can
        ignore this.
        """


class CanCollideCircleMixin(CollidedWithMixin, Sprite):
    """
    Defines a circular region collider and provides a method to check for
    collision.
    """
    radius: float = 1

    def collides_with(self, other: 'CanCollideCircleMixin'):
        """
        Check if this sprite collides with another sprite.

        Both sprites must be CanCollideCircleMixin sprites.
        """
        distance = (self.position - other.position).length
        collide_distance = self.radius + other.radius
        return distance <= collide_distance


class CanCollideSquareMixin(CollidedWithMixin, Sprite):
    """
    Uses the defined square on a sprite to provide a method to check for
    collision.
    """

    def collides_with(self, other: 'CanCollideSquareMixin'):
        """
        Check if this sprite collides with another sprite.

        Both sprites must be CanCollideSquareMixin sprites.
        """
        furthest_left = min(self.left, other.left)
        furthest_right = max(self.right, other.right)
        furthest_up = max(self.top, other.top)
        furthest_down = min(self.bottom, other.bottom)
        collide_distance = self.size + other.size
        return all([furthest_right - furthest_left <= collide_distance,
                    furthest_up - furthest_down <= collide_distance])


class CollisionCheckerSystem(System):
    """
    A subsystem to check for collisions after the update step of the system.

    To use, add CollisionCheckerSystem to the list of systems in ppb.run
    or the constructor of ppb.GameEngine.

    You should only use one type of collider with this system. It is not
    designed to check fallback collision types. It is allowed, however, to
    have some sprites with colliders and some without.
    """
    primed = False

    def on_update(self, event, signal):
        self.primed = True

    def on_idle(self, event, signal):
        if not self.primed:
            return
        for s1, s2 in combinations(event.scene, 2):
            if s1 is s2:
                continue
            try:
                if s1.collides_with(s2):
                    s1.on_collided_with(s2)
                    s2.on_collided_with(s1)
            except AttributeError as err:
                if getattr(s1, "collides_with", None) and getattr(s2, "collides_with", None):
                    # Has to be collided_with or user code
                    error_target = None
                    if getattr(s1, "on_collided_with", None) is not None:
                        if getattr(s2, "on_collided_with", None) is not None:
                            # this is in user code, we want to raise this.
                            raise
                        else:
                            error_target = s2
                    else:
                        error_target = s1
                    if error_target is not None:
                        raise AttributeError(f"{type(error_target)} has no collided_with function. Did you inherit from a collider?")
