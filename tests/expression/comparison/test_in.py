# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.in_exp import In
from illogical.operand.collection import Collection
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "left, right, expected",
    [
        # Truthy
        (Value(1), Collection([Value(1)]), True),
        (Collection([Value(1)]), Value(1), True),
        (Value("1"), Collection([Value("1")]), True),
        (Value(True), Collection([Value(True)]), True),
        (Value(1.1), Collection([Value(1.1)]), True),
        # Falsy
        (Value(1), Collection([Value(2)]), False),
        (Collection([Value(2)]), Value(1), False),
        (Value(1), Value(1), False),
        (Collection([Value(1)]), Collection([Value(1)]), False),
        (Value(1), Collection([Value("1")]), False),
    ],
)
def test_evaluate(left, right, expected):
    assert In(left, right).evaluate({}) == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (Value(1), Collection([Value(1)]), "In(Value(1), Collection([Value(1)]))"),
    ],
)
def test___repr__(left, right, expected):
    assert repr(In(left, right)) == expected
