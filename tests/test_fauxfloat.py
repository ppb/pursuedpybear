import math
import operator

from ppb.utils import FauxFloat

import pytest

from hypothesis import given, assume
import hypothesis.strategies as st


def get_thingy(num):
    class Thingy(FauxFloat):
        def __float__(self):
            return num

    return Thingy()


@pytest.mark.parametrize(
    "operation",
    [
        float, abs, bool, math.ceil, math.floor, math.trunc, operator.neg,
        operator.pos,
    ],
)
@given(num=st.floats(allow_nan=False, allow_infinity=False))
def test_unary_ops(operation, num):
    t = get_thingy(num)

    assert operation(t) == operation(num)


@pytest.mark.parametrize(
    "operation",
    [
        operator.lt, operator.le, operator.eq, operator.ne, operator.ge,
        operator.gt, operator.add, operator.mul, operator.sub,
    ],
)
@given(
    num=st.floats(allow_nan=False, allow_infinity=False),
    other=st.floats(allow_nan=False, allow_infinity=False),
)
def test_binary_ops(operation, num, other):
    t = get_thingy(num)

    assert operation(t, other) == operation(num, other)
    assert operation(other, t) == operation(other, t)


@pytest.mark.parametrize(
    "operation",
    [
        operator.floordiv, operator.mod, operator.truediv,
    ],
)
@given(
    num=st.floats(allow_nan=False, allow_infinity=False),
    other=st.floats(allow_nan=False, allow_infinity=False),
)
def test_binary_ops_nonzero(operation, num, other):
    assume(num != 0)
    assume(other != 0)
    t = get_thingy(num)

    assert operation(t, other) == operation(num, other)
    assert operation(other, t) == operation(other, t)


@given(
    num=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e20, max_value=1e20),
    other=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e20, max_value=1e20),
)
def test_pow(operation, num, other):
    assume(num != 0)
    assume(other != 0)
    t = get_thingy(num)

    assert operator.pow(t, other) == operator.pow(num, other)
    assert operator.pow(other, t) == operator.pow(other, t)


# round
