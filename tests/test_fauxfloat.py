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



# The use of pytest.mark.parametrize is prefered to st.sampled_from for
# operators and datatypes for 2 reasons:
# - It guarantees the parameter space is explored exhaustively.
# - It instantiates multiple tests, whose names encode the parameters, such as
#   test_binary_ops[RealFauxFloat-float-lt]
@pytest.mark.parametrize(
    "operation", [
        float, abs, bool, int, math.ceil, math.floor, math.trunc, operator.neg,
        operator.pos,
    ],
    ids=lambda op: op.__name__,
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
    ids=lambda op: op.__name__,
)
@pytest.mark.parametrize(
    "left_type, right_type", [
        (RealFauxFloat, float), (float, RealFauxFloat),
        (RealFauxFloat, RealFauxFloat),
    ],
)
@given(
    left=st.floats(allow_nan=False, allow_infinity=False),
    right=st.floats(allow_nan=False, allow_infinity=False),
)
def test_binary_ops(operation, left, left_type, right, right_type):
    if(operation in NON_ZERO_OPS):
        assume(right != 0)

    assert operation(left_type(left), right_type(right)) == operation(left, right)


@pytest.mark.parametrize(
    "base_type, exponent_type", [
        (RealFauxFloat, float), (float, RealFauxFloat),
        (RealFauxFloat, RealFauxFloat),
    ],
)
@given(
    base=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e20, max_value=1e20),
    exponent=st.floats(allow_nan=False, allow_infinity=False, min_value=-10, max_value=10),
)
def test_pow(base, base_type, exponent, exponent_type):
    assume(base != 0 and exponent != 0)

    assert operator.pow(base_type(base), exponent_type(exponent)) == operator.pow(base, exponent)


@given(
    num=st.floats(allow_nan=False, allow_infinity=False),
    digits=st.integers() | st.none(),
)
def test_round(num, digits):
    assert round(RealFauxFloat(num), digits) == round(num, digits)
