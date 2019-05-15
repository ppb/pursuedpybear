from ppb.fields import FieldMixin, typefield


def test_basic_annotation():
    class Spam(FieldMixin):
        class Fields:
            foo: str

        foo = 42

    class Eggs(Spam):
        foo = 38

    assert Spam.foo == '42'
    assert Eggs.foo == '38'


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
