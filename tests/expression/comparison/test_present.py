# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.present import Present
from illogical.operand.reference import Reference
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "operand, expected",
    [
        # Truthy
        (Value(1), True),
        (Value(1.1), True),
        (Value("1"), True),
        (Value(True), True),
        (Value(False), True),
        # Falsy
        (Reference("Missing"), False),
    ],
)
def test_evaluate(operand, expected):
    assert Present(operand).evaluate({}) == expected


@pytest.mark.parametrize(
    "operand, expected",
    [
        (Value(1), "Present(Value(1))"),
    ],
)
def test___repr__(operand, expected):
    assert repr(Present(operand)) == expected
