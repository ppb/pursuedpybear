import pytest
from ppb.fields import FieldMixin, typefield, conversionfield, virtualfield


def test_basic_annotation():
    class Spam(FieldMixin):
        class Fields:
            foo: str

        foo = 42

    class Eggs(Spam):
        foo = 38

    assert Spam.foo == '42'
    assert Eggs.foo == '38'

    assert Spam.__annotations__['foo'] == str


def test_assign_on_init():
    class Spam(FieldMixin):
        class Fields:
            foo: str

        foo = 42

    s = Spam(foo=38)

    assert Spam.foo == '42'
    assert s.foo == '38'


def test_get_set_del():
    class Spam(FieldMixin):
        class Fields:
            foo: str

    s = Spam()

    assert not hasattr(s, 'foo')

    s.foo = 42
    assert s.foo == '42'

    del s.foo
    assert not hasattr(s, 'foo')

    assert Spam.__annotations__['foo'] == str


def test_typefield():
    class Spam(FieldMixin):
        class Fields:
            foo = typefield(str)

    s = Spam()

    assert not hasattr(s, 'foo')

    s.foo = 42
    assert s.foo == '42'

    del s.foo
    assert not hasattr(s, 'foo')

    assert Spam.__annotations__['foo'] == str


def test_conversionfield():
    class Spam(FieldMixin):
        class Fields:
            @conversionfield
            def foo(value) -> float:
                return float(value) % 360

    s = Spam()

    assert not hasattr(s, 'foo')

    s.foo = 42
    assert s.foo == 42.0

    s.foo = 400
    assert s.foo == 40.0

    del s.foo
    assert not hasattr(s, 'foo')

    assert Spam.__annotations__['foo'] == float


def test_virtualfield():
    class Spam(FieldMixin):
        class Fields:
            @virtualfield
            def foo(self) -> float:
                return 42

            @foo.setter
            def foo(self, value):
                pass

    s = Spam()

    s.foo = 'foobar'
    assert s.foo == 42

    with pytest.raises(AttributeError):
        del s.foo

    assert Spam.__annotations__['foo'] == float


def test_virtualfield_noset():
    class Spam(FieldMixin):
        class Fields:
            @virtualfield
            def foo(self) -> float:
                return 42

    s = Spam()

    assert s.foo == 42

    with pytest.raises(AttributeError):
        s.foo = 'foobar'
