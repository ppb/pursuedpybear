import pytest

from ppb import GameEngine, BaseScene
import ppb.events
from ppb.assets import Asset, AssetLoadingSystem


class AssetTestScene(BaseScene):
    def on_asset_loaded(self, event, signal):
        self.ale = event
        signal(ppb.events.Quit())


def test_loading():
    a = Asset('ppb/engine.py')
    engine = GameEngine(AssetTestScene, basic_systems=[AssetLoadingSystem])
    with engine:
        engine.start()
        ats = engine.current_scene

        engine.main_loop()

        assert a.load()
        print(vars(ats))
        assert ats.ale.asset is a
        assert ats.ale.total_loaded == 1
        assert ats.ale.total_queued == 0


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
