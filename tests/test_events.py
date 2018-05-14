from pytest import fixture
from ppb.events import EventSystem, EventMixin


@fixture
def eventsystem():
    return EventSystem()


def test_events(eventsystem):
    passed_bag = None
    passed_scene = None

    class Eventable(EventMixin):
        def on_spam(self, bag, scene, refire):
            nonlocal passed_scene, passed_bag
            assert callable(refire)
            passed_bag = bag
            passed_scene = scene

    bag = object()
    scene = object()

    e = Eventable()
    eventsystem.register_object(e)

    eventsystem.fire_event('spam', bag, scene)
    assert bag is passed_bag
    assert scene is passed_scene
