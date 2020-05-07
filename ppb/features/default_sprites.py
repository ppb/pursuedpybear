import ppb


class TargetSprite(ppb.sprites.BaseSprite):
    """Sprite that moves to a given target"""
    target = ppb.Vector(0, 0)
    speed = 1.0

    def on_update(self, update_event, signal):
        offset = self.target - self.position
        distance_this_tick = self.speed * update_event.time_delta
        if offset.length <= distance_this_tick:
            self.position = self.target
        else:
            direction = offset.normalize()
            self.position += direction * self.speed * update_event.time_delta
