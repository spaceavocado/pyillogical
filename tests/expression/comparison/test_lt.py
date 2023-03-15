# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.lt import Lt
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "left, right, expected",
    [
        # Truthy
        (Value(1), Value(2), True),
        (Value(1.1), Value(1.2), True),
        (Value(1), Value(1.1), True),
        # Falsy
        (Value(1), Value(1), False),
        (Value(1.1), Value(1.1), False),
        (Value(1), Value(0), False),
        (Value(1.1), Value(1.0), False),
        # Non comparable
        (Value("Value"), Value(1), False),
    ],
)
def test_evaluate(left, right, expected):
    assert Lt(left, right).evaluate({}) == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (Value(1), Value(2), "Lt(Value(1), Value(2))"),
    ],
)
def test___repr__(left, right, expected):
    assert repr(Lt(left, right)) == expected
