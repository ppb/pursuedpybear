from ppb.fields import FieldMixin, typefield, conversionfield


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
