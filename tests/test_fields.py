from ppb.fields import FieldMixin


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
