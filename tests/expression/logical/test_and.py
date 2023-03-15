# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.evaluable import is_evaluable
from illogical.expression.logical.and_exp import And
from illogical.expression.logical.logical import InvalidLogicalExpression
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
        And(operands)


@pytest.mark.parametrize(
    "operands, expected",
    [
        # Truthy
        ([Value(True), Value(True)], True),
        ([Value(True), Value(True), Value(True)], True),
        # Falsy
        ([Value(True), Value(False)], False),
        ([Value(False), Value(True)], False),
        ([Value(False), Value(False)], False),
    ],
)
def test_evaluate(operands, expected):
    assert And(operands).evaluate({}) == expected


@pytest.mark.parametrize(
    "operands, expected",
    [
        ([Value(True), Value(True)], True),
        ([Value(True), Value(False)], False),
        ([Reference("RefA"), Value(True)], True),
        ([Reference("Missing"), Value(True)], Reference("Missing")),
        (
            [Reference("Missing"), Reference("Missing")],
            And([Reference("Missing"), Reference("Missing")]),
        ),
    ],
)
def test_simplify(operands, expected):
    operand = And(operands)
    simplified = operand.simplify({"RefA": True})

    if is_evaluable(expected):
        assert str(simplified) == str(expected)
    else:
        assert simplified == expected


@pytest.mark.parametrize(
    "operands, expected",
    [
        ([Value(True), Value(False)], 'And([Value(True), Value(False)], symbol="AND")'),
    ],
)
def test___repr__(operands, expected):
    assert repr(And(operands)) == expected
