import unittest
from unittest import mock

from pygame import Surface

from ppb import GameEngine, BaseScene
from ppb import events
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
        engine.display = mock.Mock(spec=Surface)
        engine.start()
        self.assertIs(engine.current_scene, mock_scene)


@unittest.skip
class TestEngineSceneActivate(unittest.TestCase):

    def setUp(self):
        self.mock_scene = mock.Mock(spec=BaseScene)
        self.mock_scene.background_color = (0, 0, 0)
        self.mock_scene_class = mock.Mock(return_value=self.mock_scene)
        self.engine = GameEngine(self.mock_scene_class)
        self.engine.display = mock.Mock(spec=Surface)
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


def test_scene_change_thrashing():

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

    engine = GameEngine(ParentScene,
                        systems=[Updater(time_step=0.001), Failer], fail=fail,
                        message="ParentScene should not be counting while a child exists.")
    engine.run()


def test_scene_change_no_new():

    class Scene(BaseScene):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.running = False

        def change(self):
            return super().change()

    with GameEngine(Scene, systems=[Updater, Failer], fail=lambda n: False,
                    message="Will only time out.") as ge:
        ge.run()


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


def test_change_scene_event():

    pause_was_run = mock.Mock()
    scene_start_called = mock.Mock()

    class FirstScene(BaseScene):

        def on_update(self, event, signal):
            signal(events.StartScene(new_scene=SecondScene(ge)))

        def on_scene_paused(self, event, signal):
            assert event.scene is self
            pause_was_run()

    class SecondScene(BaseScene):

        def on_scene_started(self, event, signal):
            assert event.scene == self
            scene_start_called()
            signal(events.Quit())

    class Tester(System):
        listening = False

        def on_idle(self, idle: events.Idle, signal):
            engine = idle.engine
            if self.listening:
                assert isinstance(engine.current_scene, SecondScene)
                assert len(engine.scenes) == 2
            return ()

        def on_scene_paused(self, event, signal):
            self.listening = True

    with GameEngine(FirstScene, systems=[Updater, Tester]) as ge:
        ge.register(events.Idle, "engine", ge)
        ge.run()

    pause_was_run.assert_called()
    scene_start_called.assert_called()


def test_replace_scene_event():

    class FirstScene(BaseScene):

        def on_update(self, event, signal):
            signal(events.ReplaceScene(new_scene=SecondScene(ge)))

        def on_scene_stopped(self, event, signal):
            assert event.scene is self

    class SecondScene(BaseScene):

        def on_scene_started(self, event, signal):
            assert event.scene is self

    class TestFailer(Failer):

        def __init__(self, engine):
            super().__init__(fail=self.fail, message="Will not call", engine=engine)
            self.first_scene_ended = False

        def on_scene_stopped(self, event, signal):
            if isinstance(event.scene, FirstScene):
                self.first_scene_ended = True

        def fail(self, engine) -> bool:
            if self.first_scene_ended:
                assert len(engine.scenes) == 1, "Too many scenes on stack."
                assert isinstance(engine.current_scene, SecondScene), "Wrong current scene."
                engine.signal(events.Quit())
            return False

    with GameEngine(FirstScene, systems=[Updater, TestFailer]) as ge:
        ge.run()


def test_stop_scene_event():

    test_function = mock.Mock()

    class TestScene(BaseScene):

        def on_update(self, event, signal):
            signal(events.StopScene())

        def on_scene_stopped(self, event, signal):
            assert event.scene is self
            test_function()

    with GameEngine(TestScene, systems=[Updater, Failer], fail=lambda x: False, message="Will only time out.") as ge:
        ge.run()

    test_function.assert_called()


def test_flush_events():

    ge = GameEngine(BaseScene)
    ge.signal(events.SceneStopped())
    ge.signal(events.Quit())

    assert len(ge.events) == 2

    ge.flush_events()

    assert len(ge.events) == 0


def test_idle():
    """This test confirms that Idle events work."""
    was_called = False

    class TestSystem(System):

        def on_idle(self, event: events.Idle, signal):
            global was_called
            was_called = True
            signal(events.Quit())

    with GameEngine(BaseScene, systems=[TestSystem, Failer], fail=lambda x: False, message="Can only time out.") as ge:
        ge.run()
