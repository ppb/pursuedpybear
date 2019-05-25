import math
import operator
import typing

from ppb.utils import FauxFloat

import pytest

from hypothesis import given, assume
import hypothesis.strategies as st


class RealFauxFloat(FauxFloat):
    """From the Modern Numerical Methods Real Fake Book."""
    num: float

    def __init__(self, num: typing.SupportsFloat):
        self.num = float(num)

    def __float__(self):
        return self.num



# The use of parametrize() over st.sampled_from() is deliberate.


@pytest.mark.parametrize(
    "operation",
    [
        float, abs, bool, int, math.ceil, math.floor, math.trunc, operator.neg,
        operator.pos,
    ],
)
@given(num=st.floats(allow_nan=False, allow_infinity=False))
def test_unary_ops(operation, num: float):
    assert operation(RealFauxFloat(num)) == operation(num)


NON_ZERO_OPS = [
    operator.floordiv, operator.mod, operator.truediv,
]


@pytest.mark.parametrize(
    "operation", [
        operator.lt, operator.le, operator.eq, operator.ne, operator.ge,
        operator.gt, operator.add, operator.mul, operator.sub,
    ] + NON_ZERO_OPS,
)
@given(
    num=st.floats(allow_nan=False, allow_infinity=False),
    other=st.floats(allow_nan=False, allow_infinity=False),
)
def test_binary_ops(operation, num, other):
    if(operation in NON_ZERO_OPS):
        assume(num != 0 and other != 0)

    t = RealFauxFloat(num)
    assert operation(t, other) == operation(num, other)
    assert operation(other, t) == operation(other, num)


@given(
    base=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e20, max_value=1e20),
    exponent=st.floats(allow_nan=False, allow_infinity=False, min_value=-10, max_value=10),
)
def test_pow(base, exponent):
    assume(base != 0 and exponent != 0)

    assert operator.pow(RealFauxFloat(base), exponent) == operator.pow(base, exponent)
    assert operator.pow(base, RealFauxFloat(exponent)) == operator.pow(base, exponent)


@given(
    num=st.floats(allow_nan=False, allow_infinity=False),
    digits=st.integers() | st.none(),
)
def test_round(num, digits):
    assert round(RealFauxFloat(num), digits) == round(num, digits)
