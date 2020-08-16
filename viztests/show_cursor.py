"""
Testing show_cursor

The scene order:
   1. Black background, visible cursor. (This scene explicitly sets cursor to visible.)
   2. Blue background, visible cursor. (This is a default scene with only enough code to set the click handler.)
   3. Grey background, no cursor.
   4. Black background, visible cursor. (When this scene continues, it sets itself to end the program on click.)
"""

import ppb

font = ppb.Font("resources/ubuntu_font/Ubuntu-R.ttf", size=32)

no_cursor = "No cursor should be visible."
cursor = "Cursor should be visible."


class RootScene(ppb.BaseScene):
    cursor = [no_cursor, cursor]
    _continue = "Click to continue."
    click_event = ppb.events.StopScene()

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
        signal(self.click_event)



class NoCursorScene(RootScene):
    background_color = (100, 100, 100)
    show_cursor = False


class DefaultScene(RootScene):
    click_event = ppb.events.ReplaceScene(NoCursorScene)


class ExplicitVisibleCursor(RootScene):
    background_color = (0, 0, 0)
    show_cursor = True
    click_event = ppb.events.StartScene(DefaultScene)

    def on_scene_continued(self, _, __):
        self.click_event = ppb.events.StopScene()

ppb.run(None, starting_scene=ExplicitVisibleCursor)
