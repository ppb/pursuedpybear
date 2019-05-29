from typing import Sequence
from numbers import Number

from ppb import Vector
from ppb.sprites import BaseSprite
from ppb.flags import DoNotRender


class Camera(BaseSprite):

    image = DoNotRender

    def __init__(self, viewport: Sequence[int] = (0, 0, 800, 600),
                 pixel_ratio: float = 64):
        """

        viewport: A container of origin x, origin y, width, and
                  height. The origin is the top left point of the viewport
                  measured from the top left point of the window or screen.
                  The width and height are the raw pixel measurements of the
                  viewport.
        pixel_ratio: A number defining the pixel to game unit ratio. Divide
                     the viewport dimensions by the pixel ratio to get the
                     frame in game unit terms.
        """
        super().__init__(size=0)
        # Cameras don't take up game space, thus size 0.
        self.position = Vector(0, 0)
        self.viewport_origin = Vector(viewport[0], viewport[1])
        self._viewport_width = viewport[2]
        self._viewport_height = viewport[3]
        self.viewport_offset = Vector(self.viewport_width / 2,
                                      self.viewport_height / 2)
        self.pixel_ratio = pixel_ratio

    @property
    def frame_top(self) -> Number:
        return self.position.y + self.half_height

    @property
    def frame_bottom(self) -> Number:
        return self.position.y - self.half_height

    @property
    def frame_left(self) -> Number:
        return self.position.x - self.half_width

    @property
    def frame_right(self) -> Number:
        return self.position.x + self.half_width

    @property
    def frame_height(self) -> float:
        return self.viewport_height / self.pixel_ratio

    @property
    def frame_width(self) -> float:
        return self.viewport_width / self.pixel_ratio

    @property
    def half_height(self) -> float:
        return self.frame_height / 2

    @property
    def half_width(self) -> float:
        return self.frame_width / 2

    @property
    def viewport_width(self) -> int:
        return self._viewport_width

    @viewport_width.setter
    def viewport_width(self, value: int):
        self._viewport_width = value
        self.viewport_offset = Vector(value / 2, self.viewport_height / 2)

    @property
    def viewport_height(self) -> int:
        return self._viewport_height

    @viewport_height.setter
    def viewport_height(self, value: int):
        self._viewport_height = value
        self.viewport_offset = Vector(self.viewport_width / 2, value / 2)

    def point_in_viewport(self, point: Vector) -> bool:
        px, py = point
        vpx, vpy = self.viewport_origin
        vpw = self.viewport_width
        vph = self.viewport_height
        return vpx <= px <= (vpw+vpx) and vpy <= py <= (vph+vpy)

    def in_frame(self, sprite: BaseSprite) -> bool:
        return (self.frame_left <= sprite.right and
                self.frame_right >= sprite.left and
                self.frame_top >= sprite.bottom and
                self.frame_bottom <= sprite.top
                )

    def translate_to_frame(self, point: Vector) -> Vector:
        """
        Converts a vector from pixel-based window to in-game coordinate space
        """
        # 1. Scale from pixels to game unites
        scaled = point / self.pixel_ratio
        # 2. Reposition relative to frame edges
        return Vector(self.frame_left + scaled.x, self.frame_top - scaled.y)

    def translate_to_viewport(self, point: Vector) -> Vector:
        """
        Converts a vector from in-game to pixel-based window coordinate space
        """
        # 1. Reposition based on frame edges
        # 2. Scale from game units to pixels
        return Vector(point.x - self.frame_left, self.frame_top - point.y) * self.pixel_ratio
