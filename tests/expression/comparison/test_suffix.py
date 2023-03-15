# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.suffix import Suffix
from illogical.operand.collection import Collection
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "left, right, expected",
    [
        # Truthy
        (Value("bogus"), Value("us"), True),
        # Falsy
        (Value("something"), Value("else"), False),
        # Diff types
        (Value(1), Value(1.1), False),
        (Value(1), Value("1"), False),
        (Value(1), Value(True), False),
        (Value(1.1), Value("1"), False),
        (Value(1.1), Value(True), False),
        (Value("1"), Value(True), False),
        # Collection
        (Collection([Value(1)]), Collection([Value(1)]), False),
        (Value(1), Collection([Value(1)]), False),
    ],
)
def test_evaluate(left, right, expected):
    assert Suffix(left, right).evaluate({}) == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (Value("bogus"), Value("us"), 'Suffix(Value("bogus"), Value("us"))'),
    ],
)
def test___repr__(left, right, expected):
    assert repr(Suffix(left, right)) == expected
