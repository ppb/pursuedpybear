import ppb
import math


class TargetSprite(ppb.sprites.BaseSprite):
    """Sprite that moves to a given target.

    :param target: Vector that the sprite moves towards.
    :param speed: Distance per second that the sprite travels with linear motion.
    :param exponential_speed: Fraction of the distance to the target that the sprite travels
    per second with exponential motion. Should normally be in the range [0.0, 1.0].
    :param max_speed: Maximum distance per second that the sprite can travel.
    :param min_speed: Minimum distance per second that the sprite travels when not in range of the target.
    """
    target = ppb.Vector(0, 0)
    speed = 1.0
    exponential_speed = 0.0
    max_speed = math.inf
    min_speed = -math.inf

    def on_update(self, update_event, signal):
        if self.max_speed < self.min_speed:
            raise ValueError("TargetSprite maximum speed cannot be less than minimum speed.")
        offset = self.target - self.position
        distance_to_target = offset.length
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
