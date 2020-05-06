import ppb


class TargetSprite(ppb.BaseSprite):
    """Sprite that moves to a given target"""
    target = ppb.Vector(0, 0)
    speed = 1.0

    def on_update(self, update_event, signal):
        direction = (self.position - self.target).normalize()
        self.position += direction * self.speed * update_event.time_delta
