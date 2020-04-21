"""
Renders text on a changing background.

Text should be in many colors, the background should cycle colors, and there
should be no color jaggies.
"""
import colorsys

import ppb


def hsv2rgb(h, s, v):
    return list(map(int, colorsys.hsv_to_rgb(h, s, v)))


class TextScene(ppb.BaseScene):
    elapsed = 0

    def on_scene_started(self, event, signal):
        for i, font in enumerate(('B', 'BI', 'C', 'L', 'LI', 'M', 'MI', 'R', 'RI', 'Th')):
            self.add(ppb.Sprite(
                image=ppb.Text(
                    "Hello, PPB!",
                    font=ppb.Font(f"resources/ubuntu_font/Ubuntu-{font}.ttf", size=72),
                    color=hsv2rgb(i / 10, 1.0, 75)
                ),
                position=(0, i-4.5),
            ))

    def on_update(self, event, signal):
        self.elapsed += event.time_delta
        self.background_color = hsv2rgb(self.elapsed / 10, 1.0, 200)


ppb.run(starting_scene=TextScene)
