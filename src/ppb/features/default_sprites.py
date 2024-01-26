"""
Theme: sprites with common default behaviours (motion)

Types of motion include: relative to the motion of other sprites, moving 
towards another object. 

"""

import ppb
import math


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
