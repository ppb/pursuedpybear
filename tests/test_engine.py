import unittest
from unittest import mock

from ppb import GameEngine, BaseScene


class TestEngine(unittest.TestCase):

    def test_initialize(self):
        pass

    def test_start(self):
        mock_scene = mock.Mock(spec=BaseScene)
        mock_scene_class = mock.Mock(spec=BaseScene, return_value=mock_scene)
        engine = GameEngine(mock_scene_class)
        engine.start()
        self.assertIs(engine.current_scene, mock_scene)


class TestEngineSceneActivate(unittest.TestCase):

    def setUp(self):
        self.mock_scene = mock.Mock(spec=BaseScene)
        self.mock_scene_class = mock.Mock(return_value=self.mock_scene)
        self.engine = GameEngine(self.mock_scene_class)
        self.engine.start()

    def test_continue_running(self):
        """
        Test that a Scene.change that returns (False, {}) doesn't change
        state.
        """
        self.mock_scene.change = mock.Mock(return_value=(True, {}))
        self.engine.manage_scene(*self.engine.current_scene.change())
        self.assertIs(self.engine.current_scene, self.mock_scene)

    def test_stop_scene_no_new_scene(self):
        """
        Test a Scene.change that returns (True, {}) leaves the scene
        stack empty.
        """
        self.mock_scene.change = mock.Mock(return_value=(False, {}))
        self.engine.manage_scene(*self.engine.current_scene.change())
        self.assertIsNone(self.engine.current_scene)

    def test_next_scene_none(self):
        self.mock_scene.change = mock.Mock(return_value=(False,
                                                         {"scene_class": None}
                                                         )
                                           )
        self.engine.manage_scene(*self.engine.current_scene.change())
        self.assertIs(self.engine.current_scene, self.mock_scene)
