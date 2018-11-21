from ppb import BaseSprite
from ppb import Vector
from ppb.camera import Camera


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