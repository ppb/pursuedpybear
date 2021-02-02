"""
Tests that sound managers work.

NOTE: Does not open a window.
"""
import ppb


class ExitOnFinished(ppb.SoundManager):
    time_passed = 0

    # def on_update(self, event, signal):
    #     self.time_passed += event.time_delta
    #     if self.time_passed > 1:
    #         self.resume()
    #     elif self.time_passed > 0.5:
    #         self.pause()

    def on_finished(self, event, signal):
        print(f"Sound finished {event=} {signal}")
        signal(ppb.events.Quit())


class Scene(ppb.BaseScene):
    sound = ppb.Sound("laser1.ogg")
    running = 0
    lifespan = 2

    def on_scene_started(self, event, signal):
        print("Scene start")
        signal(ppb.events.PlaySound(sound=self.sound, manager=ExitOnFinished()))


ppb.run(starting_scene=Scene)
