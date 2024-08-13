# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.evaluable import is_evaluable
from illogical.expression.logical.logical import InvalidLogicalExpression, InvalidLogicalExpressionOperand
from illogical.expression.logical.or_exp import Or
from illogical.operand.reference import Reference
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "operands, expected",
    [
        ([], InvalidLogicalExpression),
        ([Value(True)], InvalidLogicalExpression),
    ],
)
def test_constructor(operands, expected):
    with pytest.raises(expected):
        Or(operands)


@pytest.mark.parametrize(
    "operands, expected",
    [
        # Truthy
        ([Value(True), Value(True)], True),
        ([Value(True), Value(False)], True),
        ([Value(False), Value(False), Value(True)], True),
        # Falsy
        ([Value(False), Value(False)], False),
    ],
)
def test_evaluate(operands, expected):
    assert Or(operands).evaluate({}) == expected

@pytest.mark.parametrize(
    "operands",
    [
        ([Value(1), Value(True)]),
        ([Value(1), Value("bogus")]),
    ],
)
def test_evaluate_invalid_operand(operands):
    with pytest.raises(InvalidLogicalExpressionOperand):
        Or(operands).evaluate({})

@pytest.mark.parametrize(
    "operands, expected",
    [
        ([Value(True), Value(True)], True),
        ([Value(True), Value(False)], True),
        ([Value(False), Value(False)], False),
        ([Reference("RefA"), Value(False)], True),
        ([Reference("Missing"), Value(False)], Reference("Missing")),
        (
            [Reference("Missing"), Reference("Missing")],
            Or([Reference("Missing"), Reference("Missing")]),
        ),
        ([Reference("invalid"), Value(False)], Reference("invalid")),
    ],
)
def test_simplify(operands, expected):
    operand = Or(operands)
    simplified = operand.simplify({"RefA": True, "invalid": 1})

    if is_evaluable(expected):
        assert str(simplified) == str(expected)
    else:
        assert simplified == expected


@pytest.mark.parametrize(
    "operands, expected",
    [
        ([Value(True), Value(False)], 'Or([Value(True), Value(False)], symbol="OR")'),
    ],
)
def test___repr__(operands, expected):
    assert repr(Or(operands)) == expected
