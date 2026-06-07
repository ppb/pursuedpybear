"""
Theme: sprites with common default behaviours (motion)

Types of motion include: relative to the motion of other sprites, moving 
towards another object. 

"""

import ppb
import math
from ppb import keycodes
from ppb.events import KeyPressed, KeyReleased
from dataclasses import dataclass
import ppb.events as events


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
            raise ValueError(
                f"{type(self).__name__} maximum speed cannot be less than minimum speed."
            )
        if self.exponential_speed > 1.0:
            raise ValueError(
                f"{type(self).__name__} exponential speed cannot be greater than 1."
            )
        offset = self.target - self.position
        distance_to_target = offset.length
        if distance_to_target < 0.0001:
            self.position = self.target
            return
        max_distance = self.max_speed * update_event.time_delta
        min_distance = self.min_speed * update_event.time_delta
        linear_distance = self.speed * update_event.time_delta
        exponential_distance = distance_to_target * self._exponential_decay(
            update_event.time_delta
        )
        total_distance = linear_distance + exponential_distance
        total_distance = min(total_distance, max_distance)
        total_distance = max(total_distance, min_distance)
        if distance_to_target <= total_distance:
            self.position = self.target
        else:
            direction = offset.normalize()
            self.position += direction * total_distance

    def _exponential_decay(self, time_delta):
        decay_rate = 1.0 - self.exponential_speed
        remaining = decay_rate**time_delta
        decay_amount = 1.0 - remaining
        return decay_amount


@dataclass
class DirectionKeyBindings:
    """Key bindings for moving a sprite in a given direction.

    :param left: Key code for moving left.
    :param right: Key code for moving right.
    :param up: Key code for moving up.
    :param down: Key code for moving down.
    """

    left: keycodes.KeyCode
    right: keycodes.KeyCode
    up: keycodes.KeyCode
    down: keycodes.KeyCode


arrow_direction_key_bindings = DirectionKeyBindings(
    keycodes.Left, keycodes.Right, keycodes.Up, keycodes.Down
)

wasd_direction_key_bindings = DirectionKeyBindings(
    keycodes.A, keycodes.D, keycodes.W, keycodes.S
)


class KeyBoardMovementSprite(ppb.Sprite):
    """Sprite that moves up, down, left, or right in response to keyboard input.

    :param speed: Distance per second that the sprite travels with linear motion.
        Negative values cause movement in the opposite direction.
    :param key_bindings: Key bindings for moving the sprite in a given direction. Instance of DirectionKeyBindings
    """

    direction = ppb.Vector(0, 0)
    speed = 1.0

    key_bindings = arrow_direction_key_bindings

    def on_update(self, update_event, signal):
        displacement = self.direction.scale_to(self.speed * update_event.time_delta)
        self.position += displacement

    def on_key_pressed(self, key_event: KeyPressed, signal):
        if key_event.key == self.key_bindings.left:
            self.direction += ppb.Vector(-1, 0)
        if key_event.key == self.key_bindings.right:
            self.direction += ppb.Vector(1, 0)
        if key_event.key == self.key_bindings.up:
            self.direction += ppb.Vector(0, 1)
        if key_event.key == self.key_bindings.down:
            self.direction += ppb.Vector(0, -1)

    def on_key_released(self, key_event: KeyReleased, signal):
        if key_event.key == self.key_bindings.left:
            self.direction += ppb.Vector(1, 0)
        if key_event.key == self.key_bindings.right:
            self.direction += ppb.Vector(-1, 0)
        if key_event.key == self.key_bindings.up:
            self.direction += ppb.Vector(0, -1)
        if key_event.key == self.key_bindings.down:
            self.direction += ppb.Vector(0, 1)


class MouseTargetSprite(TargetSprite):
    """Sprite that treats your mouse as a moving target.

    :param speed: Distance per second that the sprite travels with linear motion.
        If you set the speed to a high number (eg 100) then the sprite can act as a cursor.
        If you set it to a lower number then it will chase the mouse menacingly.
    """
    def on_mouse_motion(self, event: events.MouseMotion, signal):
        self.target = event.position


