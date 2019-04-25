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

    scene_started_event = SceneStarted(None)
    scene_started_event.aspect_ratio = 2  # The width should be twice the height.
    # Not true in normal contexts, but easier to test.
    cam.__event__(scene_started_event, lambda x: None)
    assert cam.height == 5


def test_camera_change_frame_dimensions():
    cam = Camera()
    cam.height = 10

    # At this point, the camera knows that it doesn't know how to manipulate
    # the frame aspect ratio, so we use whatever value the user wants.
    assert cam.height == 10
    assert cam.width == 10

    scene_started_event = SceneStarted(None)
    scene_started_event.aspect_ratio = 2
    cam.__event__(scene_started_event, lambda x: None)
    # The camera should remember what the last set value was and try to preserve that.
    assert cam.height == 10
    assert cam.width == 20


    cam = Camera()
    cam.width = 30
    assert cam.width is 30
    assert cam.height is None  # Height is dynamically set. We didn't force it,
    # so we should still be none.
    cam.__event__(scene_started_event, lambda x: None)
    # Same rule: Width changed last, so we preserve it.
    assert cam.width == 30
    assert cam.height == 15


def test_viewport_definition():
    """
    We don't support multiple cameras yet, so the viewport should be a fixed
    rectangle starting at (0, 0) with the entire window width and height.

    All values are in percentage of the window or screen.

    For now, a rectangle can just be
    """
    cam = Camera()

    assert cam.viewport == (0, 0, 1, 1)


def test_camera_frame_interaction():
    """
    We want to have a tool to make determining if a particular Sprite is
    visible.
    """
    pass


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