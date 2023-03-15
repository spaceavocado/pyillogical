# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.ne import Ne
from illogical.operand.collection import Collection
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "left, right, expected",
    [
        # Same types
        (Value(1), Value(0), True),
        (Value(1), Value(1), False),
        (Value(1.1), Value(1.0), True),
        (Value(1.1), Value(1.1), False),
        (Value("1"), Value("2"), True),
        (Value("1"), Value("1"), False),
        (Value(True), Value(False), True),
        (Value(True), Value(True), False),
        # Diff types
        (Value(1), Value(1.1), True),
        (Value(1), Value("1"), True),
        (Value(1), Value(True), True),
        (Value(1.1), Value("1"), True),
        (Value(1.1), Value(True), True),
        (Value("1"), Value(True), True),
        # Collection
        (Collection([Value(1)]), Collection([Value(1)]), True),
        (Value(1), Collection([Value(1)]), True),
    ],
)
def test_evaluate(left, right, expected):
    assert Ne(left, right).evaluate({}) == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (Value(1), Value(2), "Ne(Value(1), Value(2))"),
    ],
)
def test___repr__(left, right, expected):
    assert repr(Ne(left, right)) == expected
