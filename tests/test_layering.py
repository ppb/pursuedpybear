import ppb.camera as camera
import ppb.scenes as scenes


class LayeredSprite:

    def __init__(self, layer):
        self.layer = layer


def test_layering_attribute():

    class LayeredScene(scenes.BaseScene):

        def __init__(self):
            super().__init__()
            for x in range(5):
                self.add(LayeredSprite(x))

    scene = LayeredScene()
    for lower_sprite, higher_sprite in zip(scene, list(scene)[1:]):
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
