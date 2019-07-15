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
    for lower_sprite, higher_sprite in zip(scene.sprite_layers(), list(scene.sprite_layers())[1:]):
        if isinstance(lower_sprite, camera.Camera) or isinstance(higher_sprite, camera.Camera):
            continue
        assert lower_sprite.layer < higher_sprite.layer


def test_change_layer_ints():

    test_sprite = LayeredSprite(0)
    ones = tuple(LayeredSprite(1) for _ in range(3))

    scene = scenes.BaseScene()
    scene.add(test_sprite)
    for sprite in ones:
        scene.add(sprite)

    assert list(scene.sprite_layers())[0] == test_sprite

    test_sprite.layer = 2

    assert list(scene.sprite_layers())[-1] == test_sprite


def test_defined_layers():

    class LayeredScene(scenes.BaseScene):
        defined_layers = {
            "background": 0,
            "enemies": 2,
            "players": 4,
            "bullets": 6,
        }

    scene = LayeredScene()

    assert scene.defined_layers == {"background": 0, "enemies": 2,
                                    "players": 4, "bullets": 6}


def test_defined_layers_sprites():
    class LayeredScene(scenes.BaseScene):
        defined_layers = {
            "background": 0,
            "enemies": 2,
            "players": 4,
            "bullets": 6,
        }

    scene = LayeredScene()

    scene.add(LayeredSprite("background"))
    for _ in range(3):
        scene.add(LayeredSprite("enemies"))
    scene.add(LayeredSprite("players"))
    scene.add(LayeredSprite("bullets"))

    assert [s.layer for s in scene.sprite_layers()] == ["background", "enemies",
                                                        "enemies", "enemies",
                                                        "players", "bullets"]

    assert len(list(scene.get(layer="background"))) == 1
    assert len(list(scene.get(layer="enemies"))) == 3
    assert len(list(scene.get(layer=4))) == 1


def test_layer_names():

    class LayeredScene(scenes.BaseScene):
        layer_names = ["background", "mobs", "projectiles", "particles"]

    scene = LayeredScene()

    assert scene.defined_layers == {
                                    "background": 0,
                                    "mobs": 1,
                                    "projectiles": 2,
                                    "particles": 3
                                    }

    class NamesAndDefinitions(scenes.BaseScene):
        defined_layers = {
            "background": 0,
            "back_particles": 2,
        }
        named_layers = ["mobs", "projectiles", "fore_particles"]

    scene = NamesAndDefinitions
    assert scene.defined_layers == {
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

    assert list(scene.sprite_layers())[0] == test_sprite

    class DefinedLayers(scenes.BaseScene):
        named_layers = "background", "foreground"

    scene = DefinedLayers()

    scene.add(test_sprite)

    for _ in range(2):
        scene.add(LayeredSprite("background"))
        scene.add(LayeredSprite("foreground"))

    assert test_sprite in scene.get(layer="background")


def test_named_layers_with_undefined_layer():
    class LayeredScene(scenes.BaseScene):
        defined_layers = {
            "defined_layer": 2,
            "defined_layer_2": 4
        }

    scene = LayeredScene()

    test_sprite = LayeredSprite("undefined_layer")
    scene.add(test_sprite)
    scene.add(LayeredSprite("defined_layer"))
    scene.add(LayeredSprite("defined_layer_2"))

    assert list(scene)[0] is test_sprite

    scene.defined_layer["undefined_layer"] = 6

    assert list(scene)[-1] is test_sprite


def test_default_layer_named():

    class LayeredScene(scenes.BaseScene):
        defined_layers = {
            "our_default": 5,
            "something_else": 2,
            "another": 3
        }
        _default_layer = "our_default"

    scene = LayeredScene()

    test_object = NoLayer()
    scene.add(test_object)

    assert list(scene.get(layer="our_default")) == [test_object]


def test_default_layer_set_layer():

    class LayeredScene(scenes.BaseScene):
        named_layers = ["background", "mobs", "particles"]
        _default_layer = "particles"

    scene = LayeredScene()

    scene.default_layer = "mobs"
    assert scene.default_layer == 1
