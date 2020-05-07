import unittest
import ppb
from ppb import Vector
from ppb.features.default_sprites import TargetSprite


def test_rotatable_base_sprite():
    target_sprite = TargetSprite()
    target_sprite.target = Vector(3, 4)
    target_sprite.speed = 5.0
    target_sprite.on_update(ppb.events.Update(0.2), lambda x: None)

    assert target_sprite.position.isclose((0.6, 0.8))
