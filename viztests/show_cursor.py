"""
Testing show_cursor
"""

import ppb

font = ppb.Font("resources/ubuntu_font/Ubuntu-R.ttf", size=32)

no_cursor = "No cursor should be visible."
cursor = "Cursor should be visible."


class RootScene(ppb.BaseScene):
    cursor = [no_cursor, cursor]
    _continue = "Click to continue."
    next_scene = None

    def on_scene_started(self, _, __):
        cursor_state = getattr(self, "show_cursor", True)
        self.add(
            ppb.RectangleSprite(
                image=ppb.Text(
                    " ".join((self.cursor[cursor_state], self._continue)),
                    font=font,
                    color=(255, 255, 255)
                )
            )
        )

    def on_button_pressed(self, event:ppb.events.ButtonPressed, signal):
        if self.next_scene is not None:
            signal(ppb.events.ReplaceScene(self.next_scene))
            return
        signal(ppb.events.StopScene())


class NoCursorScene(RootScene):
    background_color = (100, 100, 100)
    show_cursor = False


class DefaultScene(RootScene):
    next_scene=NoCursorScene


class ExplicitVisibleCursor(RootScene):
    background_color = (0, 0, 0)
    next_scene=DefaultScene


ppb.run(None, starting_scene=ExplicitVisibleCursor)
