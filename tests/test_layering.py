import ppb.camera as camera
import ppb.scenes as scenes


class LayeredSprite:

    def __init__(self, layer):
        self.layer = layer


class NoLayer:
    pass


def test_layering_attribute_ints():

    class LayeredScene(scenes.BaseScene):

        def __init__(self):
            super().__init__()
            for x in range(5):
                self.add(LayeredSprite(x))

    scene = LayeredScene()
    for lower_sprite, higher_sprite in zip(scene.sprites(), list(scene.sprites())[1:]):
        if isinstance(lower_sprite, camera.Camera) or isinstance(higher_sprite, camera.Camera):
            continue
        assert lower_sprite.layer < higher_sprite.layer


def test_change_layer():

    test_sprite = LayeredSprite(0)
    ones = tuple(LayeredSprite(1) for _ in range(3))

    scene = scenes.BaseScene()
    scene.add(test_sprite)
    for sprite in ones:
        scene.add(sprite)

    assert list(scene)[0] == test_sprite

    test_sprite.layer = 2

    assert list(scene)[-1] == test_sprite


def test_registered_layers():

    scene = scenes.BaseScene()

    scene.define_layer("background", 0)
    scene.define_layer("enemies", 1)
    scene.define_layer("players", 2)
    scene.define_layer("bullets", 3)

    assert scene.layers == {"background": 0, "enemies": 1, "players": 2, "bullets": 3}

    scene.add(LayeredSprite("background"))
    for _ in range(3):
        scene.add(LayeredSprite("enemies"))
    scene.add(LayeredSprite("players"))
    scene.add(LayeredSprite("bullets"))

    assert [s.layer for s in scene] == ["background", "enemies",  "enemies",
                                        "enemies", "players", "bullets"]

    assert len(list(scene.get(layer="background"))) == 1
    assert len(list(scene.get(layer="enemies"))) == 3
    assert len(list(scene.get(layer=2))) == 1


def test_registered_layers_no_value():

    scene = scenes.BaseScene()

    scene.define_layer("background")
    scene.define_layer("mobs")
    scene.define_layer("projectiles")
    scene.define_layer("particles")

    assert scene.layers == {
                            "background": 0,
                            "mobs": 1,
                            "projectiles": 2,
                            "particles": 3
                            }

    scene = scenes.BaseScene()
    scene.define_layer("background")
    scene.define_layer("mobs", 3)
    scene.define_layer("projectiles")
    scene.define_layer("back_particles", 2)
    scene.define_layer("fore_particles")

    assert scene.layers == {
                            "background": 0,
                            "back_particles": 2,
                            "mobs": 3,
                            "projectiles": 4,
                            "fore_particles": 5
                            }


def test_layering_without_layer_attribute():

    test_sprite = NoLayer()
    scene = scenes.BaseScene()

    scene.add(test_sprite)
    for x in range(1, 6):
        scene.add(LayeredSprite(x))

    assert list(scene)[0] == test_sprite

    scene = scenes.BaseScene()
    scene.define_layer("background", 0)
    scene.define_layer("foreground", 1)
    for _ in range(2):
        scene.add(LayeredSprite("background"))
        scene.add(LayeredSprite("foreground"))

    assert test_sprite in scene.get(layer="background")


def test_named_layers_with_undefined_layer():
    scene = scenes.BaseScene()

    scene.define_layer("defined_layer", 2)
    scene.define_layer("defined_layer_2", 4)

    test_sprite = LayeredSprite("undefined_layer")
    scene.add(test_sprite)
    scene.add(LayeredSprite("defined_layer"))
    scene.add(LayeredSprite("defined_layer_2"))

    assert list(scene)[0] is test_sprite

    scene.define_layer("undefined_layer", 6)

    assert list(scene)[-1] is test_sprite


def test_default_layer_named():

    scene = scenes.BaseScene()
    scene.define_layer("our_default", 5, default=True)
    scene.define_layer("something_else", 2)
    scene.define_layer("another", 2)

    test_object = NoLayer()
    scene.add(test_object)

    assert list(scene.get(layer="our_default")) == [test_object]


def test_default_layer_set_layer():

    scene = scenes.BaseScene()
    scene.define_layer("background")
    scene.define_layer("mobs")
    scene.define_layer("particles")

    scene.default_layer = "mobs"
    assert scene.default_layer == 1
