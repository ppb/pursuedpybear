import pytest

import ppb.changelib


def test_renamed_function():
    arg = None

    def func(p):
        """
        a docstring
        """
        nonlocal arg
        arg = p

    oldfunc = ppb.changelib.renamed('oldfunc', func, version='1.0')

    with pytest.deprecated_call():
        oldfunc("hello")

    assert oldfunc.__name__ == 'oldfunc'
    assert 'deprecated' in oldfunc.__doc__
    assert 'func' in oldfunc.__doc__
    assert arg == "hello"


def test_renamed_function_nodoc():
    def func(p): pass

    oldfunc = ppb.changelib.renamed('oldfunc', func, version='1.0')

    assert oldfunc.__name__ == 'oldfunc'
    assert 'deprecated' in oldfunc.__doc__
    assert 'func' in oldfunc.__doc__


def test_renamed_class():
    class Foo:
        """
        a class
        """

    oldfoo = ppb.changelib.renamed('oldfoo', Foo, version='1.0')

    with pytest.deprecated_call():
        inst = oldfoo()

    assert oldfoo.__name__ == 'oldfoo'
    assert 'deprecated' in oldfoo.__doc__
    assert 'Foo' in oldfoo.__doc__
    assert isinstance(inst, Foo)
