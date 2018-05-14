from pytest import mark
from ppb.events import EventMixin, camel_to_snake


def test_eventmixin():
    passed_bag = None
    passed_fire = None

    class Spam:
        pass

    class Eventable(EventMixin):
        def on_spam(self, bag, fire_event):
            nonlocal passed_bag, passed_fire
            passed_fire = fire_event
            passed_bag = bag
            passed_scene = scene

    bag = Spam()
    scene = object()
    fire_event = lambda: none

    e = Eventable()

    e.__event__(bag, scene, fire_event)
    assert bag is passed_bag
    assert fire_event is passed_fire


@mark.parametrize("text,expected", [
    ("CamelCase", "camel_case"),
    ("CamelCamelCase", "camel_camel_case"),
    ("Camel2Camel2Case", "camel2_camel2_case"),
    ("getHTTPResponseCode", "get_http_response_code"),
    ("get2HTTPResponseCode", "get2_http_response_code"),
    ("HTTPResponseCode", "http_response_code"),
    ("HTTPResponseCodeXYZ", "http_response_code_xyz"),
])
def test_camel_snake(text, expected):
    assert camel_to_snake(text) == expected
