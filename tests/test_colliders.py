from unittest.mock import Mock

from ppb.events import Idle
from ppb.features import collision
from ppb.sprites import BaseSprite

def test_circle_collider():
    pass


def test_square_collider():
    pass


def test_collide_checker_system():
    pass


def test_collide_checker_system_no_duplicate():
    class TestSprite(collision.CanCollideSquareMixin):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.on_collided_with: Mock = Mock()

    sprites = [TestSprite(), TestSprite()]

    collider_system = collision.CollisionCheckerSystem()

    collider_system.on_update(None, lambda x: None)  # We're simulating the engine here.
    collider_system.on_idle(Idle(0.016, sprites), lambda x: None)
    for sprite in sprites:
        sprite.on_collided_with.assert_called_once()
