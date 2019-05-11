from typing import Union
import ppb
import math
import time
from ppb.flags import DoNotRender


class Region(ppb.BaseSprite):
    @staticmethod
    def get_vector(other):
        if isinstance(other, ppb.BaseSprite):
            return other.position
        else:
            return other

    def contains(self, other):
        return False


class CircularRegion(Region):
    @property
    def radius(self):
        return max(self.right - self.left, self.top - self.bottom) / 2
    
    def contains(self, other):
        """
        Returns if other's position overlaps our region
        """
        pos = self.get_vector(other)
        return (self.position - pos).length < self.radius


class RectangularRegion(Region):
    def contains(self, other):
        pos = self.get_vector(other)
        return (
            self.left <= pos.x <= self.right
            and
            self.bottom >= pos.y >= self.top
        )


class ButtonSprite(Region):
    def on_button_pressed(self, mouse, signal):
        if self.contains(mouse.position):
            if mouse.button is ppb.buttons.Primary:
                self.do_primary(mouse, signal)
            elif mouse.button is ppb.buttons.Secondary:
                self.do_secondary(mouse, signal)
            elif mouse.button is ppb.buttons.Tertiary:
                self.do_tertiary(mouse, signal)

    def do_primary(self, mouse, signal): pass
    def do_secondary(self, mouse, signal): pass
    def do_tertiary(self, mouse, signal): pass


class MenuSprite(ButtonSprite):
    def do_primary(self, mouse, signal):
        if mouse.button is ppb.buttons.Primary:
            mouse.scene.do_select(self, signal)


class MenuScene(ppb.BaseScene):
    def __init__(self, *p, **kw):
        super().__init__(*p, background_color=(0, 0, 0), **kw)

        for s in self.get_options():
            self.add(s, tags=['option'])

        self.arrange()

    def sort_key(self, sprite):
        return sprite.image

    def arrange(self):
        pass

    def do_select(self, sprite, signal):
        """
        Do a thing when a sprite has been clicked.
        """


class CircularMenuScene(MenuScene):
    """
    Arrange its sprites in concentric rings
    """

    # Distance between each ring
    ring_increment = 1
    # The size to assume each item is
    item_size = 1

    def arrange(self):
        sprites = sorted(self.get(tag='option'), key=self.sort_key)

        # Leave the first one in the middle, if we'd have more than one ring
        if len(sprites) > 6:
            sprites.pop()

        radius = 0

        while sprites:
            radius += self.ring_increment
            circumfrence = 2 * math.pi * radius
            count = math.floor(circumfrence / self.item_size)
            ring, sprites = sprites[:count], sprites[count:]

            angle = 0
            inc = 2 * math.pi / len(ring)
            for s in ring:
                s.position = ppb.Vector(
                    math.sin(angle) * radius,
                    math.cos(angle) * radius,
                )
                angle += inc


class AnimationSprite(ppb.BaseSprite):
    def __init__(self, *p, anchor: Union[ppb.BaseSprite, ppb.Vector], pos=None, **kw):
        self.anchor = anchor
        if pos is None:
            pos = self.aposition
        super().__init__(*p, pos=pos, **kw)
        self._start_time = time.monotonic()
        self._last_time = None

    @property
    def aposition(self) -> ppb.Vector:
        """
        The anchor position.
        """
        if isinstance(self.anchor, ppb.BaseSprite):
            return self.anchor.position
        else:
            return self.anchor

    def do_start(self, signal):
        """
        Set initial conditions
        """

    def do_frame(self, dt: float, t: float, signal) -> bool:
        """
        Update the animation based on the given frame.

        Returns if there is more frame to do: True if so, False if not
        """
        return False

    def do_finish(self, signal):
        """
        Do any cleanup and trigger anything else
        """

    # We seperate these tasks on the assumption that an Update might not happen
    # every frame, and we should keep the work we do during a frame to a minimum

    def on_update(self, update, signal):
        if self._last_time is None:
            self.do_start(signal)
            self._last_time = time.monotonic() - self._start_time
        elif self._last_time is ...:
            update.scene.remove(self)
            self.do_finish(signal)

    def on_pre_render(self, pr, signal):
        t = time.monotonic() - self._start_time
        if self._last_time is None:
            pass
        elif self._last_time is ...:
            pass
        else:
            dt = t - self._last_time
            more = self.do_frame(dt, t, signal)
            if more:
                self._last_time = t
            else:
                self._last_time = ...


def clamp(left, x, right):
    return max(left, min(x, right))
