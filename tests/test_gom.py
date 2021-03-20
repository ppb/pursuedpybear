import pytest

from ppb.errors import BadChildException
from ppb.gomlib import GameObject, Children



class TestEnemy:
    pass


class TestPlayer:
    pass


class TestSubclassPlayer(TestPlayer):
    pass


class TestSprite:
    pass


def containers():
    yield GameObject()


def players():
    yield TestPlayer()
    yield TestSubclassPlayer()


def players_and_containers():
    for player in players():
        for container in containers():
            yield player, container


@pytest.fixture()
def enemies():
    return TestEnemy(), TestEnemy()


@pytest.mark.parametrize("player, container", players_and_containers())
def test_add_methods(container, player, enemies):
    container.add(player)
    for group, sprite in zip(("red", "blue"), enemies):
        container.add(sprite, [group])
    assert player in container
    for enemy in enemies:
        assert enemy in container


@pytest.mark.parametrize("container", containers())
def test_add_type_to_game_object(container):
    with pytest.raises(BadChildException):
        container.add(TestSprite)


@pytest.mark.parametrize("player, container", players_and_containers())
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

    with pytest.raises(TypeError):
        container.get()


@pytest.mark.parametrize("player, container", players_and_containers())
def test_get_with_string_tags(container, player):
    """Test that addings a string instead of an array-like throws."""
    with pytest.raises(TypeError):
        container.add(player, "player")


@pytest.mark.parametrize("player, container", players_and_containers())
def test_remove_methods(container, player, enemies):
    container.add(player, ["test"])
    container.add(enemies[0], ["test"])
    container.add(enemies[1], ["blue"])
    assert player in container
    assert enemies[0] in container
    assert enemies[1] in container

    container.remove(player)

    assert player not in container
    for kind in container.children.kinds():
        assert player not in container.get(kind=kind)
    for tag in container.children.tags():
        assert player not in container.get(tag=tag)

    assert enemies[0] in container
    assert enemies[0] in container.get(tag="test")
    assert enemies[1] in container


@pytest.mark.parametrize("player", players())
def test_collection_methods(player, enemies):
    container = Children()
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
