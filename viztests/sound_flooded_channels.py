"""
Fires off more sounds than the default number of sound channels. Should
complete without error.

NOTE: Does not open a window.
"""
import ppb


class Scene(ppb.BaseScene):
    sound = ppb.Sound("laser1.ogg")
    running = 0
    lifespan = 4

    def on_scene_started(self, event, signal):
        print("Scene start")
        for _ in range(17):
            signal(ppb.events.PlaySound(sound=self.sound))

    def on_update(self, event, signal):
        self.running += event.time_delta
        if self.running > self.lifespan:
            signal(ppb.events.Quit())


ppb.run(starting_scene=Scene, basic_systems=(
    ppb.systems.Updater, ppb.systems.SoundController, ppb.assetlib.AssetLoadingSystem
))
