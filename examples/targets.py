import logging
import ppb
from ppb import Vector


class MoverMixin(ppb.BaseSprite):
    velocity = Vector(0, 0)

    def on_update(self, update, signal):
        self.position += self.velocity * update.time_delta


class Player(MoverMixin, ppb.BaseSprite):
    def on_key_press(self, event, signal):
        ... # Set movement, using WASD

    def on_button_press(self, event, signal):
        if ...:  # Which mouse button
            event.scene.add(
                Bullet(pos=self.position),
                tags=['bullet']
            )


class Bullet(MoverMixin, ppb.BaseSprite):
    velocity = Vector(0, 1.0)

    def on_update(self, update, signal):
        super().on_update(update, signal)  # Execute movement

        scene = update.scene
        
        if self.position.y > scene.main_camera.frame_bottom:
            scene.remove(self)
        else:
            for target in scene.get(tag='target'):
                d = (target.position - self.position).length
                if length <= target.radius:
                    scene.remove(self)
                    scene.remote(target)
                    break


class Target(ppb.BaseSprite):
    radius = 1


class GameScene(ppb.BaseScene):
    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)

        # Set up sprites
        self.add(Player(pos=Vector(0, 0)), tags=['player'])

        # 5 targets in x = -3.75 -> 3.75, give 1/5 margin between targets 
        for x in (-2.4, -1.2, 0, 1.2, 2.4):
            self.add(Target(pos=Vector(x, 1.875)), tags=['target'])


if __name__ == "__main__":
    ppb.run(GameScene,
        logging_level=logging.DEBUG,
        window_title="Targets",
        resolution=(600, 400),
    )
