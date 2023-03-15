# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.expression.comparison.none import Non
from illogical.operand.reference import Reference
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "operand, expected",
    [
        # Truthy
        (Reference("Missing"), True),
        # Falsy
        (Value(1), False),
        (Value(1.1), False),
        (Value("1"), False),
        (Value(True), False),
        (Value(False), False),
    ],
)
def test_evaluate(operand, expected):
    assert Non(operand).evaluate({}) == expected


@pytest.mark.parametrize(
    "operand, expected",
    [
        (Reference("Missing"), 'Non(Reference("Missing"))'),
    ],
)
def test___repr__(operand, expected):
    assert repr(Non(operand)) == expected
