# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.evaluable import is_evaluable
from illogical.expression.logical.logical import InvalidLogicalExpression, InvalidLogicalExpressionOperand
from illogical.expression.logical.nor import Nor
from illogical.expression.logical.not_exp import Not
from illogical.expression.logical.xor import Xor
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
        Xor(operands)


@pytest.mark.parametrize(
    "operands, expected",
    [
        # Truthy
        ([Value(True), Value(False)], True),
        ([Value(False), Value(True)], True),
        ([Value(True), Value(False), Value(False)], True),
        ([Value(False), Value(True), Value(False)], True),
        ([Value(False), Value(False), Value(True)], True),
        # Falsy
        ([Value(True), Value(True)], False),
        ([Value(False), Value(False)], False),
        ([Value(True), Value(True), Value(False)], False),
        ([Value(True), Value(False), Value(True)], False),
        ([Value(True), Value(True), Value(True)], False),
    ],
)
def test_evaluate(operands, expected):
    assert Xor(operands).evaluate({}) == expected

@pytest.mark.parametrize(
    "operands",
    [
        ([Value(1), Value(True)]),
        ([Value(1), Value("bogus")]),
    ],
)
def test_evaluate_invalid_operand(operands):
    with pytest.raises(InvalidLogicalExpressionOperand):
        Xor(operands).evaluate({})


@pytest.mark.parametrize(
    "operands, expected",
    [
        ([Value(False), Value(False)], False),
        ([Reference("RefA"), Value(True)], False),
        (
            [Reference("Missing"), Value(True), Reference("Missing")],
            Nor([Reference("Missing"), Reference("Missing")]),
        ),
        (
            [Reference("Missing"), Value(True), Value(False)],
            Not(Reference("Missing")),
        ),
        ([Reference("RefA"), Reference("RefA"), Value(True)], False),
        ([Value(False), Reference("Missing")], Reference("Missing")),
        (
            [Reference("Missing"), Reference("Missing")],
            Xor([Reference("Missing"), Reference("Missing")]),
        ),
        ([Value(False), Reference("invalid")], Reference("invalid")),
    ],
)
def test_simplify(operands, expected):
    operand = Xor(operands)
    simplified = operand.simplify({"RefA": True, "invalid": 1})

    if is_evaluable(expected):
        assert str(simplified) == str(expected)
    else:
        assert simplified == expected


@pytest.mark.parametrize(
    "operands, expected",
    [
        (
            [Value(True), Value(False)],
            "Xor([Value(True), Value(False)]"
            + ', symbol="XOR", not_symbol="NOT", nor_symbol="NOR")',
        ),
    ],
)
def test___repr__(operands, expected):
    assert repr(Xor(operands)) == expected
