from ppb import Vector
from ppb import BaseSprite


class Camera(BaseSprite):

    def __init__(self, viewport=(0, 0, 800, 600), pixel_ratio=80):
        """

        viewport: A container of origin x, origin y, width, and
                  height in pixel space.
        pixel_ratio: An number defining the pixel to game space ratio.
                     Effectively a "zoom".
        """
        super().__init__(size=0)
        # Cameras don't take up game space, thus size 0.
        self.position = Vector(0, 0)
        self.viewport_origin = Vector(viewport[0], viewport[1])
        self.viewport_width = viewport[2]
        self.viewport_height = viewport[3]
        self.viewport_offset = Vector(self.viewport_width / 2,
                                      self.viewport_height / 2)
        self.pixel_ratio = pixel_ratio
        self.frame_width = self.viewport_width / pixel_ratio
        self.frame_height = self.viewport_height / pixel_ratio
        self.half_width = self.frame_width / 2
        self.half_height = self.frame_height / 2

    @property
    def frame_top(self):
        return self.position.y - self.half_height

    @property
    def frame_bottom(self):
        return self.position.y + self.half_height

    @property
    def frame_left(self):
        return self.position.x - self.half_width

    @property
    def frame_right(self):
        return self.position.x + self.half_width

    def point_in_viewport(self, point:Vector) -> bool:
        px, py = point
        vpx, vpy = self.viewport_origin
        vpw = self.viewport_width
        vph = self.viewport_height
        return vpx <= px <= vpw and vpy <= py <= vph

    def in_frame(self, sprite: BaseSprite):
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
