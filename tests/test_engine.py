import time
import unittest
from unittest import mock

from pygame import Surface

from ppb import GameEngine, BaseScene
from ppb.systems import System
from ppb.systems import Updater
from ppb.testutils import Failer
from ppb.testutils import Quitter

CONTINUE = True
STOP = False


@unittest.skip
class TestEngine(unittest.TestCase):

    def test_initialize(self):
        pass

    def test_start(self):
        mock_scene = mock.Mock(spec=BaseScene)
        mock_scene.background_color = (0, 0, 0)
        mock_scene_class = mock.Mock(spec=BaseScene, return_value=mock_scene)
        engine = GameEngine(mock_scene_class)
        engine.start()
        self.assertIs(engine.current_scene, mock_scene)


@unittest.skip
class TestEngineSceneActivate(unittest.TestCase):

    def setUp(self):
        self.mock_scene = mock.Mock(spec=BaseScene)
        self.mock_scene.background_color = (0, 0, 0)
        self.mock_scene_class = mock.Mock(return_value=self.mock_scene)
        self.engine = GameEngine(self.mock_scene_class)
        self.engine.start()

    def test_continue_running(self):
        """
        Test that a Scene.change that returns (True, {}) doesn't change
        state.
        """
        self.mock_scene.change = mock.Mock(return_value=(CONTINUE, {}))
        self.engine.manage_scene()
        self.assertIs(self.engine.current_scene, self.mock_scene)

    def test_stop_scene_no_new_scene(self):
        """
        Test a Scene.change that returns (False, {}) leaves the scene
        stack empty.
        """
        self.mock_scene.change = mock.Mock(return_value=(STOP, {}))
        self.engine.manage_scene()
        self.assertIsNone(self.engine.current_scene)

    def test_next_scene_none(self):
        self.mock_scene.change = mock.Mock(return_value=(CONTINUE,
                                                         {"scene_class": None}
                                                         )
                                           )
        self.engine.manage_scene()
        self.assertIs(self.engine.current_scene, self.mock_scene)


def test_scene_change():

    class ChildScene(BaseScene):
        count = 0
        def on_update(self, event, signal):
            print(f"Child")
            self.running = False

    class ParentScene(BaseScene):
        count = 0
        fired = False

        def on_update(self, event, signal):
            if not self.fired:
                self.next = ChildScene
                self.fired = True
            else:
                self.count += 1
            print(f"Parent {self.count}")
            if self.count >= 5:
                self.running = False

    def fail(engine):
        try:
            parent = engine.scenes[0]
        except IndexError:
            return False
        if parent.count > 0 and engine.current_scene != parent:
            return True

    failer = Failer(fail=fail, message="ParentScene should not be counting while a child exists.")
    engine = GameEngine(ParentScene, systems=[Updater(time_step=0.001), failer])
    engine.run()


def test_signal():

    engine = GameEngine(BaseScene, systems=[Quitter])
    engine.run()
    assert not engine.running


def test_contexts():
    class FakeRenderer(System):

        def __init__(self, **kwargs):
            self.entered = False
            self.exited = False

        def __enter__(self):
            self.entered = True

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.exited = True

    engine = GameEngine(BaseScene, systems=[FakeRenderer, Quitter])
    engine.run()
    for system in engine.systems:
        if isinstance(system, FakeRenderer):
            break
    else:
        system = None
        assert isinstance(system, FakeRenderer)
    assert system.entered
    assert system.exited
