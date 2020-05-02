from pytest import mark
from pytest import raises

from ppb.errors import BadEventHandlerException
from ppb.utils import camel_to_snake

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
