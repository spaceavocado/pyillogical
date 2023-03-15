# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.eq import Eq
from illogical.operand.collection import Collection
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "left, right, expected",
    [
        # Same types
        (Value(1), Value(1), True),
        (Value(1.1), Value(1.1), True),
        (Value("1"), Value("1"), True),
        (Value(True), Value(True), True),
        (Value(False), Value(False), True),
        # # Diff types
        (Value(1), Value(1.1), False),
        (Value(1), Value("1"), False),
        (Value(1), Value(True), False),
        (Value(1.1), Value("1"), False),
        (Value(1.1), Value(True), False),
        (Value("1"), Value(True), False),
        # Collections
        (Collection([Value(1)]), Collection([Value(1)]), False),
        (Value(1), Collection([Value(1)]), False),
    ],
)
def test_evaluate(left, right, expected):
    assert Eq(left, right).evaluate({}) == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (Value(1), Value(2), "Eq(Value(1), Value(2))"),
    ],
)
def test___repr__(left, right, expected):
    assert repr(Eq(left, right)) == expected
