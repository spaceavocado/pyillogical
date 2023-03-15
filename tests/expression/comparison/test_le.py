# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.le import Le
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "left, right, expected",
    [
        # Truthy
        (Value(1), Value(1), True),
        (Value(1.1), Value(1.1), True),
        (Value(0), Value(1), True),
        (Value(1.0), Value(1.1), True),
        (Value(1), Value(1.1), True),
        # Falsy
        (Value(1), Value(0), False),
        (Value(1.1), Value(1.0), False),
        # Non comparable
        (Value("value"), Value(1), False),
    ],
)
def test_evaluate(left, right, expected):
    assert Le(left, right).evaluate({}) == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (Value(1), Value(2), "Le(Value(1), Value(2))"),
    ],
)
def test___repr__(left, right, expected):
    assert repr(Le(left, right)) == expected
