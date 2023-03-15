# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.prefix import Prefix
from illogical.operand.collection import Collection
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "left, right, expected",
    [
        # Truthy
        (Value("bo"), Value("bogus"), True),
        # Falsy
        (Value("bo"), Value("something"), False),
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
    assert Prefix(left, right).evaluate({}) == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (Value("bo"), Value("bogus"), 'Prefix(Value("bo"), Value("bogus"))'),
    ],
)
def test___repr__(left, right, expected):
    assert repr(Prefix(left, right)) == expected
