import dataclasses
from unittest import mock

from ppb import GameEngine, BaseScene, Vector
from ppb import events
from ppb.systemslib import System
from ppb.systems import Updater
from ppb.testutils import Failer
from ppb.testutils import Quitter

CONTINUE = True
STOP = False


def test_engine_initial_scene():
    mock_scene = mock.Mock(spec=BaseScene)
    mock_scene.background_color = (0, 0, 0)
    mock_scene_class = mock.Mock(spec=BaseScene, return_value=mock_scene)
    engine = GameEngine(mock_scene_class)
    engine.start()
    assert engine.current_scene is mock_scene


def test_signal():

    engine = GameEngine(BaseScene, basic_systems=[Quitter])
    engine.run()
    assert not engine.running


def test_signal_once():

    engine = GameEngine(BaseScene, basic_systems=[Quitter])
    with engine:
        engine.start()
        engine.loop_once()
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

    engine = GameEngine(BaseScene, basic_systems=[FakeRenderer, Quitter])
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
            signal(events.StartScene(new_scene=SecondScene()))

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

    with GameEngine(FirstScene, basic_systems=[Updater, Tester]) as ge:
        def extend(event):
            event.engine = ge
        ge.register(events.Idle, extend)
        ge.run()

    pause_was_run.assert_called()
    scene_start_called.assert_called()


def test_change_scene_event_no_kwargs():

    pause_was_run = mock.Mock()
    scene_start_called = mock.Mock()

    class FirstScene(BaseScene):

        def on_update(self, event, signal):
            signal(events.StartScene(new_scene=SecondScene))

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

    with GameEngine(FirstScene, basic_systems=[Updater, Tester]) as ge:
        def extend(event):
            event.engine = ge
        ge.register(events.Idle, extend)
        ge.run()

    pause_was_run.assert_called()
    scene_start_called.assert_called()


def test_replace_scene_event():

    class FirstScene(BaseScene):

        def on_update(self, event, signal):
            signal(events.ReplaceScene(new_scene=SecondScene()))

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

    with GameEngine(FirstScene, basic_systems=[Updater, TestFailer]) as ge:
        ge.run()


def test_stop_scene_event():

    test_function = mock.Mock()

    class TestScene(BaseScene):

        def on_update(self, event, signal):
            signal(events.StopScene())

        def on_scene_stopped(self, event, signal):
            assert event.scene is self
            test_function()

    with GameEngine(TestScene, basic_systems=[Updater, Failer], fail=lambda x: False, message="Will only time out.") as ge:
        ge.run()

    test_function.assert_called()


def test_flush_events():

    ge = GameEngine(BaseScene)
    ge.signal(events.SceneStopped())
    ge.signal(events.Quit())

    assert len(ge.events) == 2

    ge._flush_events()

    assert len(ge.events) == 0


def test_event_extension():

    @dataclasses.dataclass
    class TestEvent:
        pass

    class TestSystem(System):

        def __init__(self, *, engine, **_):
            super().__init__(engine=engine, **_)
            engine.register(TestEvent, self.event_extension)

        def on_update(self, event, signal):
            signal(TestEvent())
            signal(events.Quit())

        def on_test_event(self, event, signal):
            assert event.test_value == "Red"

        def event_extension(self, event):
            event.test_value = "Red"

    with GameEngine(BaseScene, basic_systems=[TestSystem, Updater, Failer], message="Will only time out.", fail=lambda x: False) as ge:
        ge.run()


def test_extending_all_events():

    def all_extension(event):
        event.test_value = "pursuedpybear"

    @dataclasses.dataclass
    class TestEvent:
        pass

    class TestScene(BaseScene):

        def on_update(self, event, signal):
            assert event.test_value == "pursuedpybear"

        def on_mouse_motion(self, event, signal):
            assert event.test_value == "pursuedpybear"

        def on_test_event(self, event, signal):
            assert event.test_value == "pursuedpybear"

    ge = GameEngine(TestScene)
    ge.start()  # We need test scene instantiated.
    ge.register(..., all_extension)

    ge.signal(events.Update(0.01))
    ge.publish()

    ge.signal(events.MouseMotion(Vector(0, 0), Vector(0, 0), Vector(0, 1), []))
    ge.publish()

    ge.signal(TestEvent())
    ge.publish()


def test_idle():
    """This test confirms that Idle events work."""
    was_called = False

    class TestSystem(System):

        def on_idle(self, event: events.Idle, signal):
            global was_called
            was_called = True
            signal(events.Quit())

    with GameEngine(BaseScene, basic_systems=[Failer], systems=[TestSystem], fail=lambda x: False, message="Can only time out.") as ge:
        ge.run()
