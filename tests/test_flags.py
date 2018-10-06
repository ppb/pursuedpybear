import inspect
from ppb.flags import Flag


def test_docstring():
    class TestFlag(Flag):
        "This is a docstring"

    assert inspect.getdoc(TestFlag) == "This is a docstring"


def test_subclass():
     class SpecialFlag(Flag, abstract=True): pass
     class TestFlag(SpecialFlag): pass

     assert isinstance(TestFlag, SpecialFlag)
