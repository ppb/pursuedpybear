import dataclasses
from unittest import mock

import pytest

from ppb import GameEngine, Scene, Vector
from ppb import events
from ppb.systemslib import System
from ppb.systems import Updater
from ppb.testutils import Failer
from ppb.testutils import Quitter
from ppb.gomlib import GameObject

CONTINUE = True
STOP = False


def scenes():
    yield Scene
    yield Scene()
    yield Scene(background_color=(0, 0, 0))


@pytest.mark.parametrize("scene", scenes())
def test_engine_initial_scene(scene):
    engine = GameEngine(scene)
    assert len(engine.children._scenes) == 0
    engine.start()
    assert len(engine.children._scenes) == 1


def test_game_engine_with_scene_class():
    props = {
        "background_color": (69, 69, 69),
        "show_cursor": False
    }
    with GameEngine(Scene, basic_systems=[Quitter], scene_kwargs=props) as ge:
        ge.run()

        assert ge.current_scene.background_color == props["background_color"]
        assert ge.current_scene.show_cursor == props["show_cursor"]


def test_game_engine_with_instantiated_scene():
    scene = Scene()

    with GameEngine(scene, basic_systems=[Quitter]) as ge:
        ge.run()

        assert ge.current_scene == scene


def test_signal():

    engine = GameEngine(Scene, basic_systems=[Quitter])
    engine.run()
    assert not engine.running


def test_signal_once():

    engine = GameEngine(Scene, basic_systems=[Quitter])
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

    engine = GameEngine(Scene, basic_systems=[FakeRenderer, Quitter])
    engine.run()
    for system in engine.children._systems:
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

    class FirstScene(Scene):

        def on_update(self, event, signal):
            signal(events.StartScene(new_scene=SecondScene()))

        def on_scene_paused(self, event, signal):
            assert event.scene is self
            pause_was_run()

    class SecondScene(Scene):

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

    with GameEngine(FirstScene, basic_systems=[Updater, Tester, Failer],
                    fail=lambda x: False, message=None) as ge:
        def extend(event):
            event.engine = ge
        ge.register(events.Idle, extend)
        ge.run()

    pause_was_run.assert_called()
    scene_start_called.assert_called()


def test_change_scene_event_no_kwargs():

    pause_was_run = mock.Mock()
    scene_start_called = mock.Mock()

    class FirstScene(Scene):

        def on_update(self, event, signal):
            signal(events.StartScene(new_scene=SecondScene))

        def on_scene_paused(self, event, signal):
            assert event.scene is self
            pause_was_run()

    class SecondScene(Scene):

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

    with GameEngine(FirstScene, basic_systems=[Updater, Tester, Failer],
                    fail=lambda x: False, message=None) as ge:
        def extend(event):
            event.engine = ge
        ge.register(events.Idle, extend)
        ge.run()

    pause_was_run.assert_called()
    scene_start_called.assert_called()


def test_replace_scene_event():

    class FirstScene(Scene):

        def on_update(self, event, signal):
            signal(events.ReplaceScene(new_scene=SecondScene()))

        def on_scene_stopped(self, event, signal):
            assert event.scene is self

    class SecondScene(Scene):

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
                assert len(engine.children._scenes) == 1, "Too many scenes on stack."
                assert isinstance(engine.current_scene, SecondScene), "Wrong current scene."
                engine.signal(events.Quit())
            return False

    with GameEngine(FirstScene, basic_systems=[Updater, TestFailer]) as ge:
        ge.run()


def test_stop_scene_event():

    test_function = mock.Mock()

    class TestScene(Scene):

        def on_update(self, event, signal):
            signal(events.StopScene())

        def on_scene_stopped(self, event, signal):
            assert event.scene is self
            test_function()

    with GameEngine(TestScene, basic_systems=[Updater, Failer], fail=lambda x: False, message="Will only time out.") as ge:
        ge.run()

    test_function.assert_called()


def test_flush_events():

    ge = GameEngine(Scene)
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

    with GameEngine(Scene, basic_systems=[TestSystem, Updater, Failer], message="Will only time out.", fail=lambda x: False) as ge:
        ge.run()


def test_extending_all_events():

    def all_extension(event):
        event.test_value = "pursuedpybear"

    @dataclasses.dataclass
    class TestEvent:
        pass

    class TestScene(Scene):

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
            nonlocal was_called
            was_called = True
            signal(events.Quit())

    with GameEngine(Scene, basic_systems=[Failer], systems=[TestSystem], fail=lambda x: False, message="Can only time out.") as ge:
        ge.run()


def test_tree():
    """Tests deep trees"""
    call_count = 0

    class TestSystem(System):
        def __init__(self, **props):
            super().__init__(**props)
            o = Agent()
            self.add(o)
            for _ in range(5):
                c = Agent()
                o.add(c)
                o = c

        def on_idle(self, event: events.Idle, signal):
            nonlocal call_count
            call_count += 1
            signal(events.Quit())

    class Agent(GameObject):
        def on_idle(self, event: events.Idle, signal):
            nonlocal call_count
            call_count += 1

    with GameEngine(Scene, basic_systems=[Failer], systems=[TestSystem], fail=lambda x: False, message="Can only time out.") as ge:
        ge.run()

    assert call_count == 7


def test_target_events():
    class Test: pass

    call_count = 0

    class Targetted(GameObject):
        def on_test(self, event, signal):
            nonlocal call_count
            call_count += 1

    class Untargetted(GameObject):
        def on_test(self, event, signal):
            assert False

    target = Targetted()

    def setup(scene):

        scene.add(target)
        scene.add(Untargetted())

    with GameEngine(setup, basic_systems=[Failer], systems=[], fail=lambda x: False, message="Can only time out.") as ge:
        ge.signal(Test(), targets=[target])
        ge.signal(events.Quit())
        ge.run()

    assert call_count == 1
