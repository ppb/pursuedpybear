from ppb import BaseSprite
from ppb import Vector
from ppb.camera import Camera

from hypothesis import given, assume
import hypothesis.strategies as st


def test_camera_move():
    cam = Camera()
    cam.position = Vector(500, 500)
    assert cam.position == Vector(500, 500)
    cam.position += Vector(100, 100)
    assert cam.position == Vector(600, 600)


def test_camera_viewport():
    cam = Camera(viewport=(0, 0, 800, 600))
    assert cam.point_in_viewport(Vector(400, 400))
    assert not cam.point_in_viewport(Vector(900, 600))
    assert cam.viewport_offset == Vector(400, 300)


def test_camera_point_in_viewport_not_at_origin():
    cam = Camera(viewport=(100, 100, 800, 600))
    assert cam.point_in_viewport(Vector(150, 650))
    assert cam.point_in_viewport(Vector(899, 300))
    assert not cam.point_in_viewport(Vector(50, 50))
    assert not cam.point_in_viewport(Vector(901, 600))


def test_camera_translate_to_frame():
    cam = Camera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.position == Vector(0, 0)
    assert cam.frame_top == 3.75
    assert cam.frame_bottom == -3.75
    assert cam.frame_left == -5
    assert cam.frame_right == 5
    assert cam.translate_to_frame(Vector(400, 300)) == Vector(0, 0)
    assert cam.translate_to_frame(Vector(560, 220)) == Vector(2, 1)
    cam.position = Vector(5, 5)
    assert cam.translate_to_frame(Vector(400, 300)) == Vector(5, -5)
    assert cam.translate_to_frame(Vector(560, 220)) == Vector(7, -4)


def test_camera_translate_to_viewport():
    cam = Camera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.position == Vector(0, 0)
    assert cam.translate_to_viewport(Vector(0, 0)) == Vector(400, 300)
    assert cam.translate_to_viewport(Vector(2, 1)) == Vector(560, 220)
    cam.position = Vector(5, 5)
    assert cam.translate_to_viewport(Vector(5, 5)) == Vector(400, 300)
    assert cam.translate_to_viewport(Vector(7, 4)) == Vector(560, 380)


def test_camera_translate_to_viewport_2():
    cam = Camera(viewport=(0, 0, 800, 600), pixel_ratio=1)
    assert cam.position == Vector(0, 0)
    assert cam.translate_to_viewport(Vector(0, 0)) == Vector(400, 300)
    assert cam.translate_to_viewport(Vector(100, 100)) == Vector(500, 200)
    assert cam.translate_to_viewport(Vector(-150, -500)) == Vector(250, 800)


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


def test_viewport_change_affects_frame_height():
    cam = Camera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.frame_left == -5
    cam.viewport_width = 400
    assert cam.frame_left == -2.5


@given(
    vp_width=st.integers(min_value=1),
    vp_height=st.integers(min_value=1),
    pixel_ratio=st.floats(min_value=1, allow_nan=False, allow_infinity=False),
    cam_x=st.floats(allow_nan=False, allow_infinity=False),
    cam_y=st.floats(allow_nan=False, allow_infinity=False),
    point_x=st.floats(allow_nan=False, allow_infinity=False),
    point_y=st.floats(allow_nan=False, allow_infinity=False),
)
def test_transfromation_roundtrip(vp_width, vp_height, pixel_ratio, cam_x, cam_y, point_x, point_y):
    cam = Camera(
        viewport=(0, 0, vp_width, vp_height),
        pixel_ratio=pixel_ratio,
    )
    cam.position = Vector(cam_x, cam_y)
    point = Vector(point_x, point_y)

    assert cam.translate_to_viewport(cam.translate_to_frame(point)) == point
    assert cam.translate_to_frame(cam.translate_to_viewport(point)) == point


@given(
    vp_width=st.integers(min_value=1),
    vp_height=st.integers(min_value=1),
    pixel_ratio=st.floats(min_value=1, allow_nan=False, allow_infinity=False),
    cam_x=st.floats(allow_nan=False, allow_infinity=False),
    cam_y=st.floats(allow_nan=False, allow_infinity=False),
    point_x=st.floats(allow_nan=False, allow_infinity=False),
    point_y=st.floats(allow_nan=False, allow_infinity=False),
    delta_x=st.floats(allow_nan=False, allow_infinity=False),
    delta_y=st.floats(allow_nan=False, allow_infinity=False),
)
def test_transfromation_movement(
    vp_width, vp_height, pixel_ratio, cam_x, cam_y, point_x, point_y, delta_x, delta_y,
):
    cam = Camera(
        viewport=(0, 0, vp_width, vp_height),
        pixel_ratio=pixel_ratio,
    )
    cam.position = Vector(cam_x, cam_y)
    point = Vector(point_x, point_y)
    delta = Vector(delta_x, delta_y)

    assume(delta.length != 0)

    point_moved = point + delta

    assert (cam.translate_to_frame(point_moved) - cam.translate_to_frame(point)).length / delta.length == pixel_ratio
    assert delta.length / (cam.translate_to_viewport(point_moved) - cam.translate_to_viewport(point)).length == pixel_ratio
