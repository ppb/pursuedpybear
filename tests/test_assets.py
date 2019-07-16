import pytest

from ppb import GameEngine, BaseScene
from ppb.assets import Asset, AssetLoadingSystem


def test_loading():
    a = Asset('ppb/engine.py')
    engine = GameEngine(BaseScene, basic_systems=[AssetLoadingSystem])
    with engine:
        engine.start()

        assert a.load()


# def test_loading_root():
#     a = Asset(...)  # TODO: find a cross-platform target in $VENV/bin
#     engine = GameEngine(BaseScene, basic_systems=[AssetLoadingSystem])
#     with engine:
#         engine.start()

#         assert a.load()


def test_missing_package():
    a = Asset('does/not/exist')
    engine = GameEngine(BaseScene, basic_systems=[AssetLoadingSystem])
    with engine:
        engine.start()

        with pytest.raises(FileNotFoundError):
            assert a.load()


def test_missing_resource():
    a = Asset('ppb/dont.touch.this')
    engine = GameEngine(BaseScene, basic_systems=[AssetLoadingSystem])
    with engine:
        engine.start()

        with pytest.raises(FileNotFoundError):
            assert a.load()


def test_parsing():
    class Const(Asset):
        def background_parse(self, data):
            return "nah"

    a = Const('ppb/flags.py')
    engine = GameEngine(BaseScene, basic_systems=[AssetLoadingSystem])
    with engine:
        engine.start()

        assert a.load() == "nah"


def test_missing_parse():
    class Const(Asset):
        def file_missing(self):
            return "igotu"

    a = Const('spam/eggs')
    engine = GameEngine(BaseScene, basic_systems=[AssetLoadingSystem])
    with engine:
        engine.start()

        assert a.load() == "igotu"


def test_instance_condense():
    a1 = Asset('ppb/engine.py')
    a2 = Asset('ppb/engine.py')

    a3 = Asset('ppb/scenes.py')

    assert a1 is a2
    assert a1 is not a3
