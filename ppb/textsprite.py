from typing import Tuple

from ppb.events import PreRender
from ppb.sprites import BaseSprite, RenderableMixin
from ppb.systems.text import Font, Text


class TextSprite(RenderableMixin, BaseSprite):
    """
    A sprite for working with text.

    TextSprite is more magical than most sprites because it tries to maintain
    its aspect ratio to the rendered text associated with it. Otherwise, it
    should fit the same API as a Renderable Rectangle Sprite.
    """
    text: str = ""
    color: Tuple[int, int, int] = (255, 229, 0)
    font: Font
    _rendered_text: str = None
    _half_height = 0
    _half_width = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.font is None:
            raise ValueError("A Font is required.")
        self.render()
        self._commands = []

    def on_pre_render(self, event: PreRender, signal):
        # Attempt to realize sprite.
        self.render()
        pass

    def render(self):
        if self._rendered_text != self.text:
            self.image = Text(self.text, font=self.font, color=self.color)
            self._rendered_text = self.text

    def realize(self):
        pass

    @property
    def top(self):
        return