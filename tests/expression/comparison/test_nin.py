# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.nin import Nin
from illogical.operand.collection import Collection
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "left, right, expected",
    [
        # Truthy
        (Value(0), Collection([Value(1)]), True),
        (Collection([Value(1)]), Value(0), True),
        (Value("0"), Collection([Value("1")]), True),
        (Value(False), Collection([Value(True)]), True),
        (Value(1.0), Collection([Value(1.1)]), True),
        (Value(1), Value(1), True),
        (Collection([Value(1)]), Collection([Value(1)]), True),
        (Value(1), Collection([Value("1")]), True),
        # Falsy
        (Value(1), Collection([Value(1)]), False),
        (Collection([Value(1)]), Value(1), False),
    ],
)
def test_evaluate(left, right, expected):
    assert Nin(left, right).evaluate({}) == expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (Value(0), Collection([Value(1)]), "Nin(Value(0), Collection([Value(1)]))"),
    ],
)
def test___repr__(left, right, expected):
    assert repr(Nin(left, right)) == expected
