from ppb.gomlib import Children


class Player:
    pass


class Obstacle:
    pass


class PowerUp:
    pass


class Coin(PowerUp):
    pass


class MegaCoin(Coin):
    pass


def test_children_inital_state():
    children = Children()

    assert len(children) == 0
    assert len(list(children.tags())) == 0
    assert len(list(children.kinds())) == 0


def test_add_child_to_children():
    children = Children()
    player = Player()

    children.add(player)

    assert len(children) == 1
    assert player in children


def test_children_kinds():
    children = Children()

    children.add(Player())
    children.add(Obstacle())
    children.add(Obstacle())
    children.add(PowerUp())

    all_kinds = list(children.kinds())
    assert Player in all_kinds
    assert Obstacle in all_kinds
    assert PowerUp in all_kinds


def test_children_kinds_contains_superkinds():
    children = Children()

    children.add(MegaCoin())

    all_kinds = list(children.kinds())
    assert MegaCoin in all_kinds
    assert Coin in all_kinds
    assert PowerUp in all_kinds


def test_children_tags():
    children = Children()

    children.add(Obstacle())
    children.add(Obstacle(), tags=["scalable"])
    children.add(Obstacle(), tags=["scalable", "explosive"])

    all_tags = list(children.tags())
    assert "scalable" in all_tags
    assert "explosive" in all_tags


def test_get_children_by_kind():
    children = Children()
    city_wall = Obstacle()
    fallen_bus = Obstacle()
    mine = Obstacle()

    for child in (city_wall, fallen_bus, mine):
        children.add(child)

    obstacles = list(children.get(kind=Obstacle))
    assert len(obstacles) == 3
    assert city_wall in obstacles
    assert fallen_bus in obstacles
    assert mine in obstacles


def test_get_children_by_kind_using_superkind():
    children = Children()
    megacoin = MegaCoin()

    children.add(megacoin)

    assert list(children.get(kind=MegaCoin)) == [megacoin]
    assert list(children.get(kind=Coin)) == [megacoin]
    assert list(children.get(kind=PowerUp)) == [megacoin]


def test_get_children_by_tag():
    children = Children()
    city_wall = Obstacle()
    fallen_bus = Obstacle()
    mine = Obstacle()

    children.add(city_wall)
    children.add(fallen_bus, tags=["scalable"])
    children.add(mine, tags=["scalable", "explosive"])

    assert list(children.get(tag="explosive")) == [mine]

    scalable_obstacles = list(children.get(tag="scalable"))
    assert len(scalable_obstacles) == 2
    assert fallen_bus in scalable_obstacles
    assert mine in scalable_obstacles


def test_get_children_by_tag_and_kind():
    children = Children()
    angry_me = Player()
    mad_bull = Player()
    volcano = Obstacle()

    children.add(angry_me, tags=["explosive"])
    children.add(mad_bull)
    children.add(volcano, tags=["explosive"])

    explosive_players = list(children.get(tag="explosive", kind=Player))
    assert explosive_players == [angry_me]


def test_remove():
    children = Children()
    angry_me = Player()

    children.add(angry_me, tags=["explosive"])

    assert angry_me in children
    assert angry_me in children.get(tag="explosive")
    assert angry_me in children.get(kind=Player)
    assert angry_me in children.get(tag="explosive", kind=Player)

    children.remove(angry_me)

    assert angry_me not in children
    assert angry_me not in children.get(tag="explosive")
    assert angry_me not in children.get(kind=Player)
    assert angry_me not in children.get(tag="explosive", kind=Player)
