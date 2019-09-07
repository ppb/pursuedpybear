from unittest.mock import Mock

from ppb.events import Idle
from ppb.features import collision
from ppb_vector import Vector


def test_circle_collider():
    sprite_1 = collision.CanCollideCircleMixin()
    sprite_2 = collision.CanCollideCircleMixin()
    assert sprite_1.collides_with(sprite_2)
    assert sprite_2.collides_with(sprite_1)

    sprite_1.position = Vector(3, 0)
    assert not sprite_1.collides_with(sprite_2)
    assert not sprite_2.collides_with(sprite_1)

    sprite_1.position = Vector(2, 0)
    assert sprite_1.collides_with(sprite_2)
    assert sprite_2.collides_with(sprite_1)


def test_square_collider():
    sprite_1 = collision.CanCollideSquareMixin(size=2)
    sprite_2 = collision.CanCollideSquareMixin(size=1)
    assert sprite_1.collides_with(sprite_2)
    assert sprite_2.collides_with(sprite_1)

    sprite_2.position = Vector(2, 0)
    assert not sprite_1.collides_with(sprite_2)
    assert not sprite_2.collides_with(sprite_1)

    sprite_2.position = Vector(1.5, 0)
    assert sprite_1.collides_with(sprite_2)
    assert sprite_2.collides_with(sprite_1)


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
