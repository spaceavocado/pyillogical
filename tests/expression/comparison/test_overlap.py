# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.overlap import Overlap
from illogical.operand.collection import Collection
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "left, right, expected",
    [
        # Truthy
        (Collection([Value(1)]), Collection([Value(1)]), True),
        (Collection([Value(1), Value(2)]), Collection([Value(1), Value(3)]), True),
        (
            Collection([Value(3), Value(2)]),
            Collection([Value(1), Value(2), Value(3)]),
            True,
        ),
        (Collection([Value("1")]), Collection([Value("1")]), True),
        (Collection([Value(True)]), Collection([Value(True)]), True),
        (Collection([Value(1.1)]), Collection([Value(1.1)]), True),
        # Falsy
        (Value(1), Collection([Value(1)]), False),
        (Collection([Value(1)]), Value(1), False),
        (Value(1), Value(1), False),
        (Collection([Value(1)]), Collection([Value(2)]), False),
    ],
)
def test_evaluate(left, right, expected):
    assert Overlap(left, right).evaluate({}) == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (
            Collection([Value(1)]),
            Collection([Value(1)]),
            "Overlap(Collection([Value(1)]), Collection([Value(1)]))",
        ),
    ],
)
def test___repr__(left, right, expected):
    assert repr(Overlap(left, right)) == expected
