from math import isclose

import hypothesis.strategies as st
from hypothesis import given, assume, note, example
import pytest

from ppb import Sprite
from ppb import Vector
from ppb.camera import Camera
from .utils import vectors


@pytest.fixture
def camera():
    return Camera(None, 10, (800, 600))


@pytest.mark.parametrize("cam", [camera])
def test_camera_move(cam):
    cam.position = Vector(500, 500)
    assert cam.position == Vector(500, 500)
    cam.position += Vector(100, 100)
    assert cam.position == Vector(600, 600)


def test_setting_in_game_dimensions(camera):
    """
    Proves setting the width and height affect each other and matches
    the calculated ratio to the viewport.
    """
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


@pytest.mark.parametrize("position, expected", [
    [Vector(0, 0), {"right": 5, "left": -5, "top": 3.75, "bottom": -3.75}],
    [Vector(0, 1), {"right": 5, "left": -5, "top": 4.75, "bottom": -2.75}],
    [Vector(15, -33), {"right": 20, "left": 10, "top": -29.25, "bottom": -36.75}]
])
def test_camera_sides(camera, position, expected):
    camera.position = position
    assert camera.left == expected["left"]
    assert camera.right == expected["right"]
    assert camera.top == expected["top"]
    assert camera.bottom == expected["bottom"]


@pytest.mark.parametrize("position, expected", [
    [Vector(0, 0), {"tl": Vector(-5, 3.75), "tr": Vector(5, 3.75), "bl": Vector(-5, -3.75), "br": Vector(5, -3.75)}],
    [Vector(3, 6), {"tl": Vector(-2, 9.75), "tr": Vector(8, 9.75), "bl": Vector(-2, 2.25), "br": Vector(8, 2.25)}],
    [Vector(85, -2), {"tl": Vector(80, 1.75), "tr": Vector(90, 1.75), "bl": Vector(80, -5.75), "br": Vector(90, -5.75)}]
])
def test_camera_corners(camera, position, expected):
    camera.position = position
    assert camera.top_left == expected["tl"]
    assert camera.top_right == expected["tr"]
    assert camera.bottom_left == expected["bl"]
    assert camera.bottom_right == expected["br"]


@pytest.mark.parametrize("position, point, expect", [
    [Vector(0, 0), Vector(-4, 3), True],
    [Vector(0, 0), Vector(-7, 1), False],
    [Vector(50, 24), Vector(46, 26), True],
    [Vector(50, 24), Vector(0, 0), False],
    [Vector(0, 0), Vector(5, 3.75), True],  # Points on the edge are visible.
    [Vector(0, 0), Vector(5, 4), False],
    [Vector(0, 0), Vector(0, 3.75), True],
])
def test_camera_point_is_visible(camera, position, point, expect):
    camera.position = position
    assert camera.point_is_visible(point) == expect


@pytest.mark.parametrize("position, point, expected", [
    [Vector(0, 0), Vector(-1, -1), Vector(320, 380)],
    [Vector(0, 0), Vector(4, -3), Vector(720, 540)],
    [Vector(0, 0), Vector(-6, 4), Vector(-80, -20)]
])
def test_camera_translate_point_to_screen(camera, position, point, expected):
    camera.position = position
    assert camera.translate_point_to_screen(point) == expected


@pytest.mark.parametrize("position, point, expected", [
    [Vector(0, 0), Vector(320, 380), Vector(-1, -1)],
    [Vector(0, 0), Vector(720, 540), Vector(4, -3)],
    [Vector(0, 0), Vector(-80, -20), Vector(-6, 4)]
])
def test_camera_translate_point_to_game_space(camera, position, point, expected):
    camera.position = position
    assert camera.translate_point_to_game_space(point) == expected


# @pytest.mark.skip(reason="Test for old camera. Will want to restore this functionality in new camera.")
# def test_sprite_in_viewport():
#     # Added the expected pixel ratio due to change in default breaking this test.
#     # 80 is the legacy value.
#     cam = OldCamera(viewport=(0, 0, 800, 600), pixel_ratio=80)
#
#     class Thing(Sprite):
#         def __init__(self, position=Vector(2, 2)):
#             super().__init__()
#             self.size = 2
#             self.position = position
#
#     sprite_in = Thing(Vector(-3, -1))
#     sprite_half_in = Thing(Vector(5, -2))
#     sprite_out = Thing(Vector(2, 5))
#
#     assert not cam.in_frame(sprite_out)
#     assert cam.in_frame(sprite_in)
#     assert cam.in_frame(sprite_half_in)
#
#
# @pytest.mark.skip("Old camera test. Will probably want to rewrite this in the future to support new camera.")
# @given(
#     vp_width=st.integers(min_value=1),
#     vp_height=st.integers(min_value=1),
#     pixel_ratio=st.floats(min_value=1, max_value=1e5, allow_nan=False, allow_infinity=False),
#     cam_pos=vectors(1e15),  # Set low to prevent loss-of-precision problems about frame size
#     point=vectors(),
# )
# @example(vp_width=2, vp_height=2, pixel_ratio=1.0, cam_pos=Vector(0.0, 0.0), point=Vector(0.0, 0.0))
# def test_transfromation_roundtrip(vp_width, vp_height, pixel_ratio, cam_pos, point):
#     cam = OldCamera(
#         viewport=(0, 0, vp_width, vp_height),
#         pixel_ratio=pixel_ratio,
#     )
#     cam.position = cam_pos
#
#     note(f"frame: ({cam.frame_left}, {cam.frame_bottom}) -> ({cam.frame_right}, {cam.frame_top})")
#
#     # Some underflow/loss of precision problems
#     assume(cam.frame_left != cam.frame_right)
#     assume(cam.frame_top != cam.frame_bottom)
#
#     note(f"point: {point}")
#
#     point_frame = cam.translate_to_frame(point)
#     note(f"point->frame: {point_frame}")
#     point_viewport = cam.translate_to_viewport(point_frame)
#     note(f"point->frame->viewport: {point_viewport}")
#     assert point_viewport.isclose(point, rel_tol=1e-5, rel_to=[cam.position])
#
#     point_viewport = cam.translate_to_viewport(point)
#     note(f"point->viewport: {point_viewport}")
#     point_frame = cam.translate_to_frame(point_viewport)
#     note(f"point->viewport->frame: {point_frame}")
#     assert point_frame.isclose(point, rel_tol=1e-5, rel_to=[cam.position])


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
