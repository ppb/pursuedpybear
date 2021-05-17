"""
Theme: sprites with common default behaviours (motion)

Types of motion include: relative to the motion of other sprites, moving
towards another object.

"""

import ppb
import math
from typing import Dict


class TargetSprite(ppb.Sprite):
    """Sprite that moves to a given target.

    :param target: Vector that the sprite moves towards.
    :param speed: Distance per second that the sprite travels with linear motion.
    Negative values cause movement away from the target.
    :param exponential_speed: Fraction of the distance to the target that the sprite travels
    per second with exponential motion. Must be less than 1.
    Negative values cause movement away from the target.
    :param max_speed: Maximum distance per second that the sprite can travel towards the target.
    Negative values cause movement away from the target.
    :param min_speed: Minimum distance per second that the sprite travels when not in range of the target.
    Non-negative values prevent movement away from the target.
    """
    target = ppb.Vector(0, 0)
    speed = 1.0
    exponential_speed = 0.0
    max_speed = math.inf
    min_speed = -math.inf

    def on_update(self, update_event, signal):
        if self.max_speed < self.min_speed:
            raise ValueError(f"{type(self).__name__} maximum speed cannot be less than minimum speed.")
        if self.exponential_speed > 1.0:
            raise ValueError(f"{type(self).__name__} exponential speed cannot be greater than 1.")
        offset = self.target - self.position
        distance_to_target = offset.length
        if distance_to_target < 0.0001:
            self.position = self.target
            return
        max_distance = self.max_speed * update_event.time_delta
        min_distance = self.min_speed * update_event.time_delta
        linear_distance = self.speed * update_event.time_delta
        exponential_distance = distance_to_target * self._exponential_decay(update_event.time_delta)
        total_distance = linear_distance + exponential_distance
        total_distance = min(total_distance, max_distance)
        total_distance = max(total_distance, min_distance)
        if distance_to_target <= total_distance:
            self.position = self.target
        else:
            direction = offset.normalize()
            self.position += direction * total_distance

    def _exponential_decay(self, time_delta):
        decay_rate = 1. - self.exponential_speed
        remaining = decay_rate ** time_delta
        decay_amount = 1. - remaining
        return decay_amount


ARROW_KEYS = {
    "up": ppb.keycodes.Up,
    "left": ppb.keycodes.Left,
    "down": ppb.keycodes.Down,
    "right": ppb.keycodes.Right,
}

WASD_KEYS = {
    "up": ppb.keycodes.W,
    "left": ppb.keycodes.A,
    "down": ppb.keycodes.S,
    "right": ppb.keycodes.D,
}


class KeyboardMovementSprite(ppb.Sprite):
    """
    Sprite that moves with keyboard movement keys.


    Example: ::

        player = KeyboardMovementSprite()

        def setup(scene):
            scene.add(player)

        ppb.run(setup=setup)

    :param initial_speed: The speed per second when the first of subsequent keypresses are made.
    :param acceleration: The increase in speed for a repeated key press.
    :param friction: The rate of decrease in speed.
    :param max_speed: Maximum speed per second that the sprite can travel in a specific direction.
    :param direction_keys: Configuration for mapping direction to keys. Requires a dictionary with
        the keys `up`, `left`, `down`, right` and value of type `ppb.keycodes.KeyCode`.
    """

    initial_speed: float = 1.0
    acceleration: float = 0.2
    friction: float = 0.8
    max_speed: float = math.inf
    direction_keys: Dict[str, ppb.keycodes.KeyCode] = ARROW_KEYS
    speed: ppb.Vector = ppb.Vector(0, 0)

    def on_update(self, update_event, signal):
        self._validate()
        self._limit_speed()
        self._stop_if_slow()
        self._slow_down(update_event.time_delta)

        self.position += self.speed * update_event.time_delta

    def on_key_pressed(self, key_event: ppb.events.KeyPressed, signal):
        self._adjust_speed(key_event)

    def _validate(self):
        if self.friction > 1 or self.friction < 0:
            raise ValueError(f"{type(self).__name__} friction must be between 0 and 1.")

        if self.initial_speed <= 0:
            raise ValueError(f"{type(self).__name__} initial speed must be a positive value.")

        if self.acceleration < 0:
            raise ValueError(f"{type(self).__name__} acceleration must be more than or equals to 0.")

        if self.max_speed <= 0:
            raise ValueError(f"{type(self).__name__} max speed must be a positive value.")

    def _slow_down(self, time_delta: float):
        self.speed = self.speed * (1 - self.friction) ** time_delta

    def _stop_if_slow(self):
        if self.speed.length < ppb.Vector(0.5, 0.5).length:
            self._reset_speed()

    def _reset_speed(self):
        self.speed = ppb.Vector(0, 0)

    def _adjust_speed(self, key_event):
        if self.speed.length > self.initial_speed:
            magnitude = (1 + self.acceleration) * self.initial_speed
        else:
            magnitude = self.initial_speed

        if key_event.key == self.direction_keys["left"]:
            change = ppb.directions.Left
        elif key_event.key == self.direction_keys["right"]:
            change = ppb.directions.Right
        elif key_event.key == self.direction_keys["up"]:
            change = ppb.directions.Up
        elif key_event.key == self.direction_keys["down"]:
            change = ppb.directions.Down
        else:
            change = None

        if change:
            self.speed += change.scale_to(magnitude)

    def _limit_speed(self):
        if self.speed.length > self.max_speed:
            self.speed = self.speed.scale_to(self.max_speed)
