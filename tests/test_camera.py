from math import isclose

import hypothesis.strategies as st
from hypothesis import given, assume, note, example
import pytest

from ppb import Sprite
from ppb import Vector
from ppb.camera import OldCamera
from ppb.camera import Camera
from .utils import vectors


@pytest.fixture
def old_camera():
    return OldCamera()


@pytest.fixture
def camera():
    return Camera(None, 10, (800, 600))


@pytest.mark.parametrize("cam", [camera, old_camera])
def test_camera_move(cam):
    cam.position = Vector(500, 500)
    assert cam.position == Vector(500, 500)
    cam.position += Vector(100, 100)
    assert cam.position == Vector(600, 600)


def test_setting_in_game_dimensions():
    """
    Proves setting the width and height affect each other and matches
    the calculated ratio to the viewport.
    """
    camera = Camera(None, 10, (800, 600))
    assert camera.width == 10
    assert camera.height == 7.5

    camera.width = 25
    assert camera.width == 25
    assert camera.height == 18.75

    camera.width = 34
    assert isclose(camera.width, 34.7826, rel_tol=0.01)
    assert isclose(camera.height, 26.08695, rel_tol=0.01)

    camera.height = 100
    assert isclose(camera.width, 133.33333, rel_tol=0.01)
    assert camera.height == 100


def test_camera_viewport():
    cam = OldCamera(viewport=(0, 0, 800, 600))
    assert cam.point_in_viewport(Vector(400, 400))
    assert not cam.point_in_viewport(Vector(900, 600))
    assert cam.viewport_offset == Vector(400, 300)


def test_camera_point_in_viewport_not_at_origin():
    cam = OldCamera(viewport=(100, 100, 800, 600))
    assert cam.point_in_viewport(Vector(150, 650))
    assert cam.point_in_viewport(Vector(899, 300))
    assert not cam.point_in_viewport(Vector(50, 50))
    assert not cam.point_in_viewport(Vector(901, 600))


def test_camera_translate_to_frame():
    cam = OldCamera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.position == Vector(0, 0)
    assert cam.frame_top == 3.75
    assert cam.frame_bottom == -3.75
    assert cam.frame_left == -5
    assert cam.frame_right == 5
    assert cam.translate_to_frame(Vector(400, 300)) == Vector(0, 0)
    assert cam.translate_to_frame(Vector(560, 220)) == Vector(2, 1)
    cam.position = Vector(5, 5)
    assert cam.translate_to_frame(Vector(400, 300)) == Vector(5, 5)
    assert cam.translate_to_frame(Vector(560, 220)) == Vector(7, 6)


def test_camera_translate_to_viewport():
    cam = OldCamera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.position == Vector(0, 0)
    assert cam.translate_to_viewport(Vector(0, 0)) == Vector(400, 300)
    assert cam.translate_to_viewport(Vector(2, 1)) == Vector(560, 220)
    cam.position = Vector(5, 5)
    assert cam.translate_to_viewport(Vector(5, 5)) == Vector(400, 300)
    assert cam.translate_to_viewport(Vector(7, 4)) == Vector(560, 380)


def test_camera_translate_to_viewport_2():
    cam = OldCamera(viewport=(0, 0, 800, 600), pixel_ratio=1)
    assert cam.position == Vector(0, 0)
    assert cam.translate_to_viewport(Vector(0, 0)) == Vector(400, 300)
    assert cam.translate_to_viewport(Vector(100, 100)) == Vector(500, 200)
    assert cam.translate_to_viewport(Vector(-150, -500)) == Vector(250, 800)


def test_sprite_in_viewport():
    # Added the expected pixel ratio due to change in default breaking this test.
    # 80 is the legacy value.
    cam = OldCamera(viewport=(0, 0, 800, 600), pixel_ratio=80)

    class Thing(Sprite):
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


def test_viewport_change_affects_frame_height():
    cam = OldCamera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.frame_left == -5
    cam.viewport_width = 400
    assert cam.frame_left == -2.5


@given(
    vp_width=st.integers(min_value=1),
    vp_height=st.integers(min_value=1),
    pixel_ratio=st.floats(min_value=1, max_value=1e5, allow_nan=False, allow_infinity=False),
    cam_pos=vectors(1e15),  # Set low to prevent loss-of-precision problems about frame size
    point=vectors(),
)
@example(vp_width=2, vp_height=2, pixel_ratio=1.0, cam_pos=Vector(0.0, 0.0), point=Vector(0.0, 0.0))
def test_transfromation_roundtrip(vp_width, vp_height, pixel_ratio, cam_pos, point):
    cam = OldCamera(
        viewport=(0, 0, vp_width, vp_height),
        pixel_ratio=pixel_ratio,
    )
    cam.position = cam_pos

    note(f"frame: ({cam.frame_left}, {cam.frame_bottom}) -> ({cam.frame_right}, {cam.frame_top})")

    # Some underflow/loss of precision problems
    assume(cam.frame_left != cam.frame_right)
    assume(cam.frame_top != cam.frame_bottom)

    note(f"point: {point}")

    point_frame = cam.translate_to_frame(point)
    note(f"point->frame: {point_frame}")
    point_viewport = cam.translate_to_viewport(point_frame)
    note(f"point->frame->viewport: {point_viewport}")
    assert point_viewport.isclose(point, rel_tol=1e-5, rel_to=[cam.position])

    point_viewport = cam.translate_to_viewport(point)
    note(f"point->viewport: {point_viewport}")
    point_frame = cam.translate_to_frame(point_viewport)
    note(f"point->viewport->frame: {point_frame}")
    assert point_frame.isclose(point, rel_tol=1e-5, rel_to=[cam.position])


# @given(
#     vp_width=st.integers(min_value=1),
#     vp_height=st.integers(min_value=1),
#     pixel_ratio=st.floats(min_value=1, max_value=1e5, allow_nan=False, allow_infinity=False),
#     cam_pos=vectors(),
#     point=vectors(),
#     delta=vectors(),
# )
# def test_transfromation_movement(
#     vp_width, vp_height, pixel_ratio, cam_pos, point, delta,
# ):
#     cam = Camera(
#         viewport=(0, 0, vp_width, vp_height),
#         pixel_ratio=pixel_ratio,
#     )
#     cam.position = cam_pos

#     assume(delta.length != 0)

#     point_moved = point + delta

#     assume(point_moved != point)  # This will happen when delta is too small to make an effect

#     note(f"point moved: {point_moved}")

#     diff = cam.translate_to_frame(point_moved) - cam.translate_to_frame(point)
#     note(f"frame diff: {diff}")
#     assert isclose(delta.length, pixel_ratio * diff.length, rel_tol=1e-4)
#     diff = cam.translate_to_viewport(point_moved) - cam.translate_to_viewport(point)
#     note(f"viewport diff: {diff}")
#     assert isclose(diff.length, pixel_ratio * delta.length, rel_tol=1e-4)
