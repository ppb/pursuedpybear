from pytest import raises, fixture

from ppb.scenes import GameObjectContainer


class TestEnemy:
    pass


class TestPlayer:
    pass


class TestSprite:
    pass


@fixture()
def container():
    return GameObjectContainer()


def test_game_object_container__add(container):
    player = TestPlayer()
    container.add(player)
    enemies = TestEnemy(), TestEnemy()
    for group, sprite in zip(("red", "blue"), enemies):
        container.add(sprite, [group])
    assert player in container
    for enemy in enemies:
        assert enemy in container


def test_game_object_container__get(container):

    player = TestPlayer()
    enemies = [TestEnemy(), TestEnemy()]
    sprite = TestSprite()
    container.add(player, ["red"])
    container.add(enemies[0])
    container.add(enemies[1], ["red"])
    container.add(sprite)

    enemy_set = set(container.get(type=TestEnemy))
    assert len(enemy_set) == 2
    for enemy in enemies:
        assert enemy in enemy_set

    player_set = set(container.get(type=TestPlayer))
    assert len(player_set) == 1
    assert player in player_set

    sprite_set = set(container.get(type=TestSprite))
    assert len(sprite_set) == 1
    assert sprite in sprite_set

    red_set = set(container.get(group="red"))
    assert len(red_set) == 2
    assert player in red_set
    assert enemies[1] in red_set

    with raises(TypeError):
        container.get()

