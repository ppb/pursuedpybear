"""
Tests loading scenes.

Should take some time to progress. This may need to be run several times to suss
out threading bugs.
"""
import ppb
import time
import random
from ppb.features.loadingscene import ProgressBarLoadingScene


class DelayedImage(ppb.Image):
    def __init__(self, name):
        self.delay_time = random.uniform(1, 7)  # This needs to happen before hinting
        print(name, self.delay_time)
        super().__init__(name)

    def background_parse(self, data):
        time.sleep(self.delay_time)
        return super().background_parse(data)


class Quitter(ppb.BaseScene):
    loop_count = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0

        self.bullet = DelayedImage('bullet.png')
        self.player = DelayedImage('player.png')
        self.target = DelayedImage('target.png')

    def on_update(self, event, signal):
        self.counter += 1
        assert self.bullet.is_loaded()
        assert self.player.is_loaded()
        assert self.target.is_loaded()
        if self.counter >= self.loop_count:
            signal(ppb.events.Quit())


class LoadingScene(ProgressBarLoadingScene):
    loaded_image = ppb.Image('target.png')

    next_scene = Quitter

    def on_asset_loaded(self, event, signal):
        print(event)
        assert event.total_queued >= 0
        assert event.total_loaded >= 0
        super().on_asset_loaded(event, signal)

    def get_progress_sprites(self):
        for x in range(-2, 3):
            yield ppb.BaseSprite(pos=ppb.Vector(x, 0))


ppb.run(starting_scene=LoadingScene)
