from typing import Callable
from typing import Iterator
from typing import Sequence

from ppb.camera import Camera
from ppb.gomlib import GameObject


class Scene(GameObject):
    # Background color, in RGB, each channel is 0-255
    background_color: Sequence[int] = (0, 0, 100)
    camera_class = Camera
    show_cursor = True

    def __init__(self, *, set_up: Callable = None, **props):
        super().__init__(**props)

        if set_up is not None:
            set_up(self)

    @property
    def main_camera(self) -> Camera:
        try:
            camera = next(self.children.get(tag="main_camera"))
        except StopIteration:
            camera = None
        return camera

    @main_camera.setter
    def main_camera(self, value: Camera):
        for camera in self.children.get(tag="main_camera"):
            self.children.remove(camera)
        self.children.add(value, tags=["main_camera"])

    def sprite_layers(self) -> Iterator:
        """
        Return an iterator of the contained Sprites in ascending layer
        order.

        Sprites are part of a layer if they have a layer attribute equal to
        that layer value. Sprites without a layer attribute are considered
        layer 0.

        This function exists primarily to assist the Renderer subsystem,
        but will be left public for other creative uses.
        """
        return sorted(self, key=lambda s: getattr(s, "layer", 0))
