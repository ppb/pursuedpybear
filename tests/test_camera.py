import pytest

from ppb import BaseSprite
from ppb import Vector
from ppb.camera import Camera
from ppb.events import SceneStarted


def test_camera_sets_height():
    """Guarantee that the height is initially set dynamically."""

    cam = Camera()

    # Going to keep the default frame of 10 game units wide.
    assert cam.width == 10
    # NotSet will be a flag so we have a sentinel value
    assert cam.height is None

    # The renderer will call this and pass in the physical aspect ratio.
    # The camera can use that ratio and it's viewport definition to determine
    # its aspect ratio.
    cam.set_aspect_ratio(2)
    assert cam.height == 5


def test_camera_change_frame_dimensions():
    """Test setting the dimensions at various points in the Camera lifetime."""
    # TODO: This looks more like a test suite to me.
    # Will probably break them into individual functions later.

    # Setting the height before the camera knows the aspect ratio.
    cam = Camera()
    cam.height = 10

    # At this point, the camera knows that it doesn't know how to manipulate
    # the frame aspect ratio, so we use whatever value the user wants.
    assert cam.height == 10
    assert cam.width == 10

    cam.set_aspect_ratio(3)  # We want to use different values for this to make sure it really works.
    # The camera should remember what the last set value was and try to preserve that.
    assert cam.height == 10
    assert cam.width == 30


    # Setting the width before the camera knows the aspect ratio.
    cam = Camera()
    cam.width = 80
    assert cam.width is 80
    assert cam.height is None  # Height is dynamically set. We didn't force it,
    # so we should still be none.
    cam.set_aspect_ratio(4)
    # Same rule: Width changed last, so we preserve it.
    assert cam.width == 80
    assert cam.height == 20


    # Setting both height and width AFTER the camera knows the aspect ratio
    cam = Camera()
    cam.set_aspect_ratio(5)
    cam.width = 500
    assert cam.width == 500
    assert cam.height == 100

    cam.height = 20
    assert cam.width == 100
    assert cam.height == 20


def test_viewport_definition():
    """
    We don't support multiple cameras yet, so the viewport should be a fixed
    rectangle starting at (0, 0) with the entire window width and height.

    All values are in percentage of the window or screen.

    For now, a rectangle can just be a tuple.
    """
    cam = Camera()

    assert cam.viewport == (0, 0, 1, 1)


def test_camera_frame_interaction():
    """
    We want to have a tool to make determining if a particular Sprite is
    visible.
    """
    cam = Camera
    cam.position = Vector(0, 0)
    cam.set_aspect_ratio(1)

    fully_in_frame_sprite = BaseSprite(position=Vector(0, 0))
    partially_in_frame_sprite = BaseSprite(position=Vector(5, 0))
    barely_in_frame_sprite = BaseSprite(position=Vector(5.4, 0))
    not_in_frame_sprite = BaseSprite(position=Vector(6, 0))

    assert cam.sprite_visible(fully_in_frame_sprite)
    assert cam.sprite_visible(partially_in_frame_sprite)
    assert cam.sprite_visible(barely_in_frame_sprite)
    assert not cam.sprite_visible(not_in_frame_sprite)


@pytest.mark.skip(reason="Old API, will be blown up with this PR.")
def test_camera_move():
    cam = Camera()
    cam.position = Vector(500, 500)
    assert cam.position == Vector(500, 500)
    cam.position += Vector(100, 100)
    assert cam.position == Vector(600, 600)


@pytest.mark.skip(reason="Old API, will be blown up with this PR.")
def test_camera_viewport():
    cam = Camera(viewport=(0, 0, 800, 600))
    assert cam.point_in_viewport(Vector(400, 400))
    assert not cam.point_in_viewport(Vector(900, 600))
    assert cam.viewport_offset == Vector(400, 300)


@pytest.mark.skip(reason="Old API, will be blown up with this PR.")
def test_camera_point_in_viewport_not_at_origin():
    cam = Camera(viewport=(100, 100, 800, 600))
    assert cam.point_in_viewport(Vector(150, 650))
    assert cam.point_in_viewport(Vector(899, 300))
    assert not cam.point_in_viewport(Vector(50, 50))
    assert not cam.point_in_viewport(Vector(901, 600))


@pytest.mark.skip(reason="Old API, will be blown up with this PR.")
def test_camera_translate_to_frame():
    cam = Camera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.position == Vector(0, 0)
    assert cam.translate_to_frame(Vector(400, 300)) == Vector(0, 0)
    assert cam.translate_to_frame(Vector(560, 220)) == Vector(2, -1)
    cam.position = Vector(5, 5)
    assert cam.translate_to_frame(Vector(400, 300)) == Vector(5, 5)
    assert cam.translate_to_frame(Vector(560, 220)) == Vector(7, 4)


@pytest.mark.skip(reason="Old API, will be blown up with this PR.")
def test_camera_translate_to_viewport():
    cam = Camera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.position == Vector(0, 0)
    assert cam.translate_to_viewport(Vector(0, 0)) == Vector(400, 300)
    assert cam.translate_to_viewport(Vector(2, -1)) == Vector(560, 220)
    cam.position = Vector(5, 5)
    assert cam.translate_to_viewport(Vector(5, 5)) == Vector(400, 300)
    assert cam.translate_to_viewport(Vector(7, 4)) == Vector(560, 220)


@pytest.mark.skip(reason="Old API, will be blown up with this PR.")
def test_sprite_in_viewport():
    # Added the expected pixel ratio due to change in default breaking this test.
    # 80 is the legacy value.
    cam = Camera(viewport=(0, 0, 800, 600), pixel_ratio=80)

    class Thing(BaseSprite):
        def __init__(self, position=Vector(2, 2)):
            super().__init__()
            self.size = 2
            self.position = position

    sprite_in = Thing(Vector(-3, -1))
    sprite_half_in = Thing(Vector(5, -2))
    sprite_out = Thing(Vector(2, 5))

    assert not cam.in_frame(sprite_out)
    assert cam.in_frame(sprite_in)
    assert cam.in_frame(sprite_half_in)


@pytest.mark.skip(reason="Old API, will be blown up with this PR.")
def test_viewport_change_affects_frame_height():
    cam = Camera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.frame_left == -5
    cam.viewport_width = 400
    assert cam.frame_left == -2.5