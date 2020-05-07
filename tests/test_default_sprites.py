import unittest
import ppb
from ppb import Vector
from ppb.features.default_sprites import TargetSprite


def test_target_sprite_linear():
    target_sprite = TargetSprite()
    target_sprite.target = Vector(3, 4)
    target_sprite.speed = 5.0
    target_sprite.on_update(ppb.events.Update(0.2), lambda x: None)

    assert target_sprite.position.isclose((0.6, 0.8))


def test_target_sprite_exponential():
    target_sprite = TargetSprite()
    target_sprite.target = Vector(3, -4)
    target_sprite.speed = 0.0
    target_sprite.exponential_speed = 0.5
    target_sprite.on_update(ppb.events.Update(2.0), lambda x: None)

    assert target_sprite.position.isclose((2.25, -3.0))


def test_target_sprite_max_speed():
    target_sprite = TargetSprite()
    target_sprite.target = Vector(-3, 4)
    target_sprite.speed = 500.
    target_sprite.exponential_speed = 0.99
    target_sprite.max_speed = 1.0
    target_sprite.on_update(ppb.events.Update(2.0), lambda x: None)

    assert target_sprite.position.isclose((-1.2, 1.6))


def test_target_sprite_min_speed():
    target_sprite = TargetSprite()
    target_sprite.target = Vector(-3, -4)
    target_sprite.speed = 0.0
    target_sprite.min_speed = 2.0
    target_sprite.on_update(ppb.events.Update(1.0), lambda x: None)

    assert target_sprite.position.isclose((-1.2, -1.6))
