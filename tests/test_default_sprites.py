import ppb
import pytest
from ppb import Vector
from ppb.features.default_sprites import TargetSprite, KeyboardMovementSprite, WASD_KEYS


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


class TestKeyboardMovementSprite:

    def test_speed(self):
        sprite = KeyboardMovementSprite()
        sprite.speed = Vector(2, 0)
        sprite.friction = 0
        sprite.on_update(ppb.events.Update(1.0), lambda x: None)

        assert sprite.position.isclose((2, 0))

    def test_max_speed(self):
        sprite = KeyboardMovementSprite()
        sprite.speed = Vector(10, 0)
        sprite.max_speed = 1.0
        sprite.friction = 0
        sprite.on_update(ppb.events.Update(1.0), lambda x: None)

        assert sprite.position.isclose((1, 0))

    def test_friction(self):
        sprite = KeyboardMovementSprite()
        sprite.speed = Vector(2, 0)
        sprite.friction = 0.5
        sprite.on_update(ppb.events.Update(1.0), lambda x: None)

        assert sprite.position.isclose((1, 0))

    def test_stop_if_slow(self):
        sprite = KeyboardMovementSprite()
        sprite.speed = Vector(0, 0.5)
        sprite.friction = 0
        sprite.on_update(ppb.events.Update(1.0), lambda x: None)

        assert sprite.position.isclose((0, 0))

    @pytest.mark.parametrize("friction", [-1, -0.1, 1.1, 2])
    def test_friction_error(self, friction):
        with pytest.raises(ValueError):
            sprite = KeyboardMovementSprite()
            sprite.friction = friction
            sprite.on_update(ppb.events.Update(1.0), lambda x: None)

    @pytest.mark.parametrize("initial_speed", [-1, 0])
    def test_initial_speed_error(self, initial_speed):
        with pytest.raises(ValueError):
            sprite = KeyboardMovementSprite()
            sprite.initial_speed = initial_speed
            sprite.on_update(ppb.events.Update(1.0), lambda x: None)

    @pytest.mark.parametrize("acceleration", [-0.1, -1])
    def test_initial_speed_error(self, acceleration):
        with pytest.raises(ValueError):
            sprite = KeyboardMovementSprite()
            sprite.acceleration = acceleration
            sprite.on_update(ppb.events.Update(1.0), lambda x: None)

    @pytest.mark.parametrize("max_speed", [-0.1, -1, 0])
    def test_initial_speed_error(self, max_speed):
        with pytest.raises(ValueError):
            sprite = KeyboardMovementSprite()
            sprite.max_speed = max_speed
            sprite.on_update(ppb.events.Update(1.0), lambda x: None)

    @pytest.mark.parametrize(
        "keypress,expected",
        [
            (ppb.keycodes.Up, (0, 1)),
            (ppb.keycodes.Down, (0, -1)),
            (ppb.keycodes.Left, (-1, 0)),
            (ppb.keycodes.Right, (1, 0)),
        ]
    )
    def test_basic_keypress(self, keypress, expected):
        sprite = KeyboardMovementSprite()
        sprite.friction = 0
        sprite.on_key_pressed(ppb.events.KeyPressed(key=keypress, mods=set()), signal=None)
        sprite.on_update(ppb.events.Update(1.0), lambda x: None)

        assert sprite.position.isclose(expected)

    @pytest.mark.parametrize(
        "keypress,expected",
        [
            (ppb.keycodes.W, (0, 1)),
            (ppb.keycodes.S, (0, -1)),
            (ppb.keycodes.A, (-1, 0)),
            (ppb.keycodes.D, (1, 0)),
        ]
    )
    def test_wasd_keypress(self, keypress, expected):
        sprite = KeyboardMovementSprite()
        sprite.direction_keys = WASD_KEYS
        sprite.friction = 0
        print(sprite.direction_keys)
        sprite.on_key_pressed(ppb.events.KeyPressed(key=keypress, mods=set()), signal=None)
        sprite.on_update(ppb.events.Update(1.0), lambda x: None)

        assert sprite.position.isclose(expected)
