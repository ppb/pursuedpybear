from unittest.mock import Mock

from pytest import fixture
from pytest import mark
from pytest import raises

from ppb.scenes import BaseScene
from ppb.scenes import GameObjectContainer


class TestEnemy:
    pass


class TestPlayer:
    pass


class TestSprite:
    pass


@fixture()
def player():
    return TestPlayer()


@fixture()
def enemies():
    return TestEnemy(), TestEnemy()


@mark.parametrize("container", (GameObjectContainer(), BaseScene(Mock())))
def test_add_methods(container, player, enemies):
    container.add(player)
    for group, sprite in zip(("red", "blue"), enemies):
        container.add(sprite, [group])
    assert player in container
    for enemy in enemies:
        assert enemy in container


@mark.parametrize("container", (GameObjectContainer(), BaseScene(Mock())))
def test_get_methods(container, player, enemies):

    sprite = TestSprite()
    container.add(player, ["red"])
    container.add(enemies[0])
    container.add(enemies[1], ["red"])
    container.add(sprite)

    enemy_set = set(container.get(kind=TestEnemy))
    assert len(enemy_set) == 2
    for enemy in enemies:
        assert enemy in enemy_set

    player_set = set(container.get(kind=TestPlayer))
    assert len(player_set) == 1
    assert player in player_set

    sprite_set = set(container.get(kind=TestSprite))
    assert len(sprite_set) == 1
    assert sprite in sprite_set

    red_set = set(container.get(tag="red"))
    assert len(red_set) == 2
    assert player in red_set
    assert enemies[1] in red_set

    with raises(TypeError):
        container.get()


@mark.parametrize("container", (GameObjectContainer(), BaseScene(Mock())))
def test_remove_methods(container, player):
    container.add(player, "test")
    assert player in container
    container.remove(player)
    assert player not in container
    assert player not in container.get(kind=TestPlayer)
    assert player not in container.get(tag="test")
