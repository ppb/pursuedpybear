from itertools import islice

import ppb.camera as camera
import ppb.scenes as scenes


class LayeredSprite:

    def __init__(self, layer):
        self.layer = layer


class NoLayer:
    pass


def test_layering_attribute():

    class LayeredScene(scenes.BaseScene):

        def __init__(self):
            super().__init__()
            for x in range(-3, 3):
                self.add(LayeredSprite(x))

    scene = LayeredScene()
    for lower_sprite, higher_sprite in zip(scene.sprite_layers(), islice(scene.sprite_layers(), 1, None)):
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

    assert next(filter(lambda s: not isinstance(s, camera.Camera), scene.sprite_layers())) is test_sprite

    test_sprite.layer = 2

    assert list(filter(lambda s: not isinstance(s, camera.Camera), scene.sprite_layers()))[-1] is test_sprite


def test_layering_without_layer_attribute():

    test_sprite = NoLayer()
    scene = scenes.BaseScene()

    scene.add(test_sprite)
    for x in range(1, 6):
        scene.add(LayeredSprite(x))

    assert next(filter(lambda s: not isinstance(s, camera.Camera), scene.sprite_layers())) is test_sprite
