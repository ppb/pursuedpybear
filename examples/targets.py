import logging
import ppb
from ppb import Vector
from ppb import keycodes
from ppb import Sound
from ppb.events import PlaySound


class MoverMixin(ppb.BaseSprite):
    velocity = Vector(0, 0)

    def on_update(self, update, signal):
        self.position += self.velocity * update.time_delta


class Player(MoverMixin, ppb.BaseSprite):
    # We handle movement by mapping each key to a velocity vector
    # and adding it on press and subtracting it on release.
    left_vector = Vector(-1, 0)
    right_vector = Vector(1, 0)
    _rotation = 180

    fire_sound = Sound('laser1.ogg')

    def on_key_pressed(self, event, signal):
        if event.key in (keycodes.A, keycodes.Left):
            self.velocity += self.left_vector
        elif event.key in (keycodes.D, keycodes.Right):
            self.velocity += self.right_vector
        elif event.key is keycodes.Space:
            self._fire_bullet(event.scene, signal)

    def on_key_released(self, event, signal):
        if event.key in (keycodes.A, keycodes.Left):
            self.velocity -= self.left_vector
        elif event.key in (keycodes.D, keycodes.Right):
            self.velocity -= self.right_vector

    def on_button_pressed(self, event, signal):
        if event.button is ppb.buttons.Primary:
            self._fire_bullet(event.scene, signal)

    def _fire_bullet(self, scene, signal):
        signal(PlaySound(self.fire_sound))
        scene.add(
            Bullet(pos=self.position),
            tags=['bullet']
        )


class Bullet(MoverMixin, ppb.BaseSprite):
    velocity = Vector(0, 2)
    _rotation = 180

    def on_update(self, update, signal):
        super().on_update(update, signal)  # Execute movement

        scene = update.scene

        if self.position.y > scene.main_camera.frame_top:
            scene.remove(self)
        else:
            for target in scene.get(tag='target'):
                d = (target.position - self.position).length
                if d <= target.radius:
                    scene.remove(self)
                    scene.remove(target)
                    break


class Target(ppb.BaseSprite):
    radius = 0.5


class GameScene(ppb.BaseScene):
    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)

        # Set up sprites
        self.add(Player(pos=Vector(0, 0)), tags=['player'])

        # 5 targets in x = -3.75 -> 3.75, with margin
        for x in (-3, -1.5, 0, 1.5, 3):
            self.add(Target(pos=Vector(x, 1.875)), tags=['target'])


if __name__ == "__main__":
    ppb.run(
        starting_scene=GameScene,
        log_level=logging.DEBUG,
    )
