from math import isclose

import hypothesis.strategies as st
from hypothesis import given, assume, note, example
import pytest

from ppb import Sprite
from ppb import Vector
from ppb.camera import Camera
from ppb.sprites import BaseSprite
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


@pytest.mark.parametrize("input_width, expected_width, expected_height", [
    [10, 10, 7.5],
    [25, 25, 18.75],
    [34, 34, 25.5],
    [133, 133, 100]
])
def test_setting_in_game_dimensions_width(camera, input_width, expected_width, expected_height):
    """
    Proves setting the width and height affect each other and matches
    the calculated ratio to the viewport.
    """
    camera.width = input_width
    assert isclose(camera.width, expected_width, rel_tol=0.01)
    assert isclose(camera.height, expected_height, rel_tol=0.01)


@pytest.mark.parametrize("input_height, expected_width, expected_height", [
    [7.5, 10, 7.5],
    [18.75, 25, 18.75],
    [25.5, 34, 25.5],
    [100, 133.33333, 100]
])
def test_setting_in_game_dimensions_height(camera, input_height, expected_width, expected_height):
    """
    Proves setting the width and height affect each other and matches
    the calculated ratio to the viewport.
    """
    camera.height = input_height
    assert isclose(camera.width, expected_width, rel_tol=0.01)
    assert isclose(camera.height, expected_height, rel_tol=0.01)


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
def test_camera_translate_point_to_screen_valid_vectors(camera, position, point, expected):
    camera.position = position
    assert camera.translate_point_to_screen(point) == expected

@pytest.mark.parametrize("point", [
  [(1.0, 1.0)],
  [{"x": 1.0, "y": 1.0}],
  [(1000000.0, -1.0)],
  [[1.0, 1.0]],
])
def test_camera_translate_point_to_screen_invalid_vectors(camera, point):
    with pytest.raises(TypeError) as excinfo:
        camera.translate_point_to_screen(point)


@pytest.mark.parametrize("position, point, expected", [
    [Vector(0, 0), Vector(320, 380), Vector(-1, -1)],
    [Vector(0, 0), Vector(720, 540), Vector(4, -3)],
    [Vector(0, 0), Vector(-80, -20), Vector(-6, 4)]
])
def test_camera_translate_point_to_game_space(camera, position, point, expected):
    camera.position = position
    assert camera.translate_point_to_game_space(point) == expected


@pytest.mark.parametrize("input_position, expected", [
    [Vector(-3, 1), True],  # Fully inside the camera's view
    [Vector(5, -2), True],  # partially inside the camera's view
    [Vector(2, 6), False],  # well outside the Camera's view.
    [Vector(6, 0), False],  # Outside with edges touching (horizontal)
    [Vector(0, 4.75), False],  # Outside with edges touching (vertical)
])
def test_sprite_in_view(camera, input_position, expected):

    class Thing(Sprite):
        size = 2
        position = input_position

    test_sprite = Thing()
    assert camera.sprite_in_view(test_sprite) == expected


@pytest.mark.parametrize("input_position, expected", [
    [Vector(0, 0), True],
    [Vector(5, 0), True],
    [Vector(0, 3.75), True],
    [Vector(10, 10), False]
])
def test_sprite_in_view_no_dimensions(camera, input_position, expected):
    test_sprite = BaseSprite(position=input_position)

    assert camera.sprite_in_view(test_sprite) == expected


@given(
    vp_width=st.integers(min_value=100, max_value=15000),
    vp_height=st.integers(min_value=100, max_value=15000),
    target_width=st.floats(min_value=1, max_value=1e5, allow_nan=False, allow_infinity=False),
    cam_pos=vectors(1e15),  # Set low to prevent loss-of-precision problems about frame size
    point=vectors(),
)
@example(vp_width=2, vp_height=2, target_width=1.0, cam_pos=Vector(0.0, 0.0), point=Vector(0.0, 0.0))
@example(vp_width=1, vp_height=1, target_width=1.0000000000222042, cam_pos=Vector(0.0, 0.0), point=Vector(0.0, 0.0))
def test_transformation_roundtrip(vp_width, vp_height, target_width, cam_pos, point):
    cam = Camera(None, target_width, (vp_width, vp_height))
    cam.position = cam_pos

    note(f"frame: ({cam.left}, {cam.bottom}) -> ({cam.right}, {cam.top})")

    # Some underflow/loss of precision problems
    assume(cam.left != cam.right)
    assume(cam.top != cam.bottom)

    note(f"point: {point}")

    point_frame = cam.translate_point_to_screen(point)
    note(f"point->frame: {point_frame}")
    point_viewport = cam.translate_point_to_game_space(point_frame)
    note(f"point->frame->viewport: {point_viewport}")
    assert point_viewport.isclose(point, rel_tol=1e-5, rel_to=[cam.position])

    point_viewport = cam.translate_point_to_game_space(point)
    note(f"point->viewport: {point_viewport}")
    point_frame = cam.translate_point_to_screen(point_viewport)
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
