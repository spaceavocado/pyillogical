# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.gt import Gt
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "left, right, expected",
    [
        # Truthy
        (Value(2), Value(1), True),
        (Value(1.2), Value(1.1), True),
        (Value(1.1), Value(1), True),
        # Falsy
        (Value(1), Value(1), False),
        (Value(1.1), Value(1.1), False),
        (Value(0), Value(1), False),
        (Value(1.0), Value(1.1), False),
        # Non comparable
        (Value("value"), Value(1), False),
    ],
)
def test_evaluate(left, right, expected):
    assert Gt(left, right).evaluate({}) == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (Value(1), Value(2), "Gt(Value(1), Value(2))"),
    ],
)
def test___repr__(left, right, expected):
    assert repr(Gt(left, right)) == expected
