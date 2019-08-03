import ppb
import time
from ppb.features.loadingscene import ProgressBarLoadingScene


class DelayedImage(ppb.Image):
    delay_time = 1

    def background_parse(self, data):
        time.sleep(self.delay_time)
        return self.background_parse(data)


class Quitter(ppb.BaseScene):
    """
    System for running test. Limits the engine to a single loop.
    """

    loop_count = 20

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0

        self.bullet = DelayedImage('bullet.png')
        self.player = DelayedImage('player.png')
        self.target = DelayedImage('target.png')

    def on_idle(self, event, signal):
        self.counter += 1
        if self.counter >= self.loop_count:
            signal(ppb.events.Quit())


class LoadingScene(ProgressBarLoadingScene):
    loaded_image = ppb.Image('target.png')

    next_scene = Quitter

    def get_progress_sprites(self):
        for x in range(-2, 2):
            yield ppb.BaseSprite(pos=ppb.Vector(x, 0))


ppb.run(starting_scene=LoadingScene)
