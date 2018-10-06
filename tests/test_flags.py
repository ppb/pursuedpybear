import inspect
import pytest
from ppb.flags import Flag


def test_docstring():
    class TestFlag(Flag):
        "This is a docstring"

    assert inspect.getdoc(TestFlag) == "This is a docstring"


def test_subclass():
     class SpecialFlag(Flag, abstract=True): pass
     class TestFlag(SpecialFlag): pass

     assert isinstance(TestFlag, SpecialFlag)


def test_instantiate():
    class TestFlag(Flag): pass

    with pytest.raises(TypeError):
        TestFlag()

    dup = type(TestFlag)()
    assert dup is TestFlag


def test_abstract_instantiate():
     class SpecialFlag(Flag, abstract=True): pass

     with pytest.raises(TypeError):
        SpecialFlag()


def test_comparison():
     class FlagA(Flag): pass
     class FlagB(Flag): pass

     assert FlagA is FlagA
     assert FlagB is not FlagA
     assert FlagA == FlagA
     assert FlagB != FlagA

