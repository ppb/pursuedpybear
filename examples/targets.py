import logging
import ppb
from ppb import Vector


class Player(ppb.BaseSprite):
    def on_key_press(self, event, signal):
        ... # Set movement, using WASD

    def on_button_press(self, event, signal):
        ... # Create bullet

    def on_update(self, update, signal):
        ... # Execute movement


class Bullet(ppb.BaseSprite):
    def on_update(self, update, signal):
        ... # Move, check for out-of-bounds


class Target(ppb.BaseSprite):
    pass


class GameScene(ppb.BaseScene):
    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)

        # Set up sprites
        self.add(Player(pos=Vector(0, 0)), tags=['player'])

        # 5 targets in x = -3.75 -> 3.75, give 1/5 margin between targets 
        for x in (-2.4, -1.2, 0, 1.2, 2.4):
            self.add(Target(pos=Vector(x, 1.875)), tags=['target'])

    def on_update(self, update, signal):
        ... # Check for collisions between bullets and targets


def main():
    ppb.run(GameScene,
        logging_level=logging.DEBUG,
        window_title="Targets",
        resolution=(600, 400),
    )

if __name__ == "__main__":
    main()
