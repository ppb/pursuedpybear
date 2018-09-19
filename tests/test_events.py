from pytest import mark
from pytest import raises

from ppb.events import BadEventHandlerException
from ppb.events import camel_to_snake
from ppb.events import EventMixin


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

    bag = Spam()
    fire_event = lambda: None

    e = Eventable()

    e.__event__(bag, fire_event)
    assert bag is passed_bag
    assert fire_event is passed_fire


def test_event_mixin_with_bad_signature():

    class BadSpam:
        pass


    class Spam:
        pass


    class Eventable(EventMixin):
        def on_spam(self, spam_event):
            pass

        def on_bad_spam(self, bad_spam_event, signal):
            raise TypeError

    e = Eventable()

    with raises(BadEventHandlerException):
        e.__event__(Spam(), lambda x: None)

    with raises(TypeError) as exception_info:
        e.__event__(BadSpam(), lambda x: None)

    exec = exception_info.value
    assert not isinstance(exec, BadEventHandlerException)


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
