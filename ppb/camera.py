from typing import Sequence
from typing import Union

from ppb import Vector
from ppb.sprites import BaseSprite
from ppb.flags import DoNotRender

class Camera(BaseSprite):

    image = DoNotRender

    def __init__(self, viewport: Sequence[int]=(0, 0, 800, 600),
                 pixel_ratio: float=80):
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
    def frame_top(self) -> Union[int, float]:
        return self.position.y - self.half_height

    @property
    def frame_bottom(self) -> Union[int, float]:
        return self.position.y + self.half_height

    @property
    def frame_left(self) -> Union[int, float]:
        return self.position.x - self.half_width

    @property
    def frame_right(self) -> Union[int, float]:
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
        return vpx <= px <= vpw and vpy <= py <= vph

    def in_frame(self, sprite: BaseSprite) -> bool:
        return (self.frame_left <= sprite.right and
                self.frame_right >= sprite.left and
                self.frame_top <= sprite.bottom and
                self.frame_bottom >= sprite.top
                )

    def translate_to_frame(self, point:Vector) -> Vector:
        offset = (point - self.viewport_offset) * (1/self.pixel_ratio)
        return self.position + offset

    def translate_to_viewport(self, point:Vector) -> Vector:
        offset = (point - self.position) * self.pixel_ratio
        return self.viewport_offset + offset
