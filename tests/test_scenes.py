from unittest.mock import Mock

from pytest import fixture
from pytest import mark
from pytest import raises

from ppb.scenes import BaseScene
from ppb.camera import Camera


@fixture()
def scene():
    return BaseScene()


def test_main_camera(scene):
    assert scene.main_camera is None

    new_cam = Camera(None, 25, (800, 600))

    scene.main_camera = new_cam

    assert scene.main_camera == new_cam
    assert new_cam in scene


def test_class_attrs():
    class BackgroundScene(BaseScene):
        background_color = (0, 4, 2)

    scene = BackgroundScene()
    assert scene.background_color == (0, 4, 2)

    scene = BackgroundScene(background_color=(2, 4, 0))
    assert scene.background_color == (2, 4, 0)
