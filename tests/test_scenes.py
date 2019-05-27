from unittest.mock import Mock

from pytest import fixture
from pytest import mark
from pytest import raises

from ppb.scenes import BaseScene
from ppb.camera import Camera
from ppb.scenes import GameObjectCollection


class TestEnemy:
    pass


class TestPlayer:
    pass


class TestSubclassPlayer(TestPlayer):
    pass


class TestSprite:
    pass


def containers():
    yield GameObjectCollection()
    yield BaseScene()


def players():
    yield TestPlayer()
    yield TestSubclassPlayer()


def players_and_containers():
    for player in players():
        for container in containers():
            yield player, container


@fixture()
def enemies():
    return TestEnemy(), TestEnemy()


@fixture()
def scene():
    return BaseScene()


@mark.parametrize("player, container", players_and_containers())
def test_add_methods(container, player, enemies):
    container.add(player)
    for group, sprite in zip(("red", "blue"), enemies):
        container.add(sprite, [group])
    assert player in container
    for enemy in enemies:
        assert enemy in container


@mark.parametrize("player, container", players_and_containers())
def test_get_methods(container, player, enemies):

    sprite = TestSprite()
    container.add(player, ["red"])
    container.add(enemies[0])
    container.add(enemies[1], ["red"])
    container.add(sprite)

    assert set(container.get(kind=TestEnemy)) == set(enemies)
    assert set(container.get(kind=TestPlayer)) == {player}
    assert set(container.get(kind=TestSprite)) == {sprite}

    assert set(container.get(tag="red")) == {player, enemies[1]}

    assert set(container.get(tag="this doesn't exist")) == set()

    with raises(TypeError):
        container.get()


@mark.parametrize("player, container", players_and_containers())
def test_get_with_string_tags(container, player):
    """Test that addings a string instead of an array-like throws."""
    with raises(TypeError):
        container.add(player, "player")


@mark.parametrize("player, container", players_and_containers())
def test_remove_methods(container, player, enemies):
    container.add(player, ["test"])
    container.add(enemies[0], ["test"])
    container.add(enemies[1], ["blue"])
    assert player in container
    assert enemies[0] in container
    assert enemies[1] in container

    container.remove(player)

    assert player not in container
    for kind in container.kinds:
        assert player not in container.get(kind=kind)
    for tag in container.tags:
        assert player not in container.get(tag=tag)

    assert enemies[0] in container
    assert enemies[0] in container.get(tag="test")
    assert enemies[1] in container


@mark.parametrize("player", players())
def test_collection_methods(player, enemies):
    container = GameObjectCollection()
    container.add(player)
    container.add(enemies[0])

    # Test __len__
    assert len(container) == 2

    # Test __contains__
    assert player in container
    assert enemies[1] not in container

    # Test __iter__
    for game_object in container:
        assert game_object is player or game_object is enemies[0]


def test_main_camera(scene):

    assert isinstance(scene.main_camera, Camera)
    old_cam = scene.main_camera
    new_cam = Camera()

    scene.main_camera = new_cam

    assert scene.main_camera == new_cam
    assert old_cam not in scene
    assert new_cam in scene


def test_class_attrs():
    class BackgroundScene(BaseScene):
        background_color = (0, 4, 2)

    scene = BackgroundScene()
    assert scene.background_color == (0, 4, 2)

    scene = BackgroundScene(background_color=(2, 4, 0))
    assert scene.background_color == (2, 4, 0)
