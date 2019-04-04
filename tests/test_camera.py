from hypothesis import given, note, strategies as st

from ppb import BaseSprite
from ppb import Vector
from ppb.camera import Camera
from ppb.testutils import integer_vectors, vectors


ONE_K = 1024
ONE_M = ONE_K * ONE_K


def cameras():
    return st.builds(
        lambda offset, diagonal: Camera(viewport=(*offset, *(offset+diagonal))),
        integer_vectors(min_value=-ONE_M, max_value=ONE_M),
        integer_vectors(min_value=2, max_value=ONE_M),
    )


@given(diagonal=integer_vectors(min_value=2, max_value=ONE_M))
def test_camera_viewport(diagonal: Vector):
    x, y = diagonal
    cam = Camera(viewport=(0, 0, x, y))
    assert cam.point_in_viewport(0.5 * diagonal)
    assert not cam.point_in_viewport(diagonal + (100, 100))
    assert cam.viewport_offset == 0.5 * diagonal


def test_camera_point_in_viewport_not_at_origin():
    cam = Camera(viewport=(100, 100, 800, 600))
    assert cam.point_in_viewport(Vector(150, 650))
    assert cam.point_in_viewport(Vector(899, 300))
    assert not cam.point_in_viewport(Vector(50, 50))
    assert not cam.point_in_viewport(Vector(901, 600))


def test_camera_translate_to_frame():
    cam = Camera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.position == Vector(0, 0)
    assert cam.translate_to_frame(Vector(400, 300)) == Vector(0, 0)
    assert cam.translate_to_frame(Vector(560, 220)) == Vector(2, -1)
    cam.position = Vector(5, 5)
    assert cam.translate_to_frame(Vector(400, 300)) == Vector(5, 5)
    assert cam.translate_to_frame(Vector(560, 220)) == Vector(7, 4)


def test_camera_translate_to_viewport():
    cam = Camera(viewport=(0, 0, 800, 600), pixel_ratio=80)
    assert cam.position == Vector(0, 0)
    assert cam.translate_to_viewport(Vector(0, 0)) == Vector(400, 300)
    assert cam.translate_to_viewport(Vector(2, -1)) == Vector(560, 220)
    cam.position = Vector(5, 5)
    assert cam.translate_to_viewport(Vector(5, 5)) == Vector(400, 300)
    assert cam.translate_to_viewport(Vector(7, 4)) == Vector(560, 220)


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
