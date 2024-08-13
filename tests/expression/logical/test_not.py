# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest
from illogical.expression.logical.logical import InvalidLogicalExpressionOperand
from illogical.evaluable import is_evaluable
from illogical.expression.logical.not_exp import Not
from illogical.operand.reference import Reference
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "operand, expected",
    [
        (Value(True), False),
        (Value(False), True),
    ],
)
def test_evaluate(operand, expected):
    assert Not(operand).evaluate({}) == expected


def test_evaluate_invalid():
    with pytest.raises(InvalidLogicalExpressionOperand):
        Not(Value(1)).evaluate({})


@pytest.mark.parametrize(
    "operand, expected",
    [
        (Value(True), False),
        (Value(False), True),
        (Reference("RefA"), False),
        (Reference("Missing"), Not(Reference("Missing"))),
    ],
)
def test_simplify(operand, expected):
    operand = Not(operand)
    simplified = operand.simplify({"RefA": True})

    if is_evaluable(expected):
        assert str(simplified) == str(expected)
    else:
        assert simplified == expected


@pytest.mark.parametrize(
    "operand, expected",
    [
        (Value(True), 'Not(Value(True), symbol="NOT")'),
    ],
)
def test___repr__(operand, expected):
    assert repr(Not(operand)) == expected
