from ppb import GameEngine, BaseScene
from ppb.testutils import Quitter
from ppb.events import Update
from ppb.features.twophase import TwoPhaseMixin, TwoPhaseSystem, Commit


def test_twophase():
    events = []

    class TestScene(BaseScene, TwoPhaseMixin):
        flag = False

        def on_update(self, event, signal):
            nonlocal events
            self.stage_changes(flag=True)
            events.append(type(event))

        def on_commit(self, event, signal):
            nonlocal events
            super().on_commit(event, signal)
            events.append(type(event))

    with GameEngine(TestScene, basic_systems=[TwoPhaseSystem, Quitter]) as engine:
        engine.signal(Update(time_delta=0.1))
        engine.run()

    assert engine.current_scene.flag
    assert events == [Update, Commit]
