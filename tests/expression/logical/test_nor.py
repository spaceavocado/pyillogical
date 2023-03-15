# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.evaluable import is_evaluable
from illogical.expression.logical.logical import InvalidLogicalExpression
from illogical.expression.logical.nor import Nor
from illogical.expression.logical.not_exp import Not
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
        Nor(operands)


@pytest.mark.parametrize(
    "operands, expected",
    [
        # Truthy
        ([Value(False), Value(False)], True),
        ([Value(False), Value(False), Value(False)], True),
        # Falsy
        ([Value(True), Value(True)], False),
        ([Value(True), Value(False)], False),
        ([Value(False), Value(True)], False),
    ],
)
def test_evaluate(operands, expected):
    assert Nor(operands).evaluate({}) == expected


@pytest.mark.parametrize(
    "operands, expected",
    [
        ([Value(False), Value(False)], True),
        ([Value(True), Value(True)], False),
        ([Value(True), Value(False)], False),
        ([Reference("RefA"), Value(False)], False),
        ([Reference("Missing"), Value(True)], False),
        ([Reference("Missing"), Value(False)], Not(Reference("Missing"))),
        (
            [Reference("Missing"), Reference("Missing")],
            Nor([Reference("Missing"), Reference("Missing")]),
        ),
    ],
)
def test_simplify(operands, expected):
    operand = Nor(operands)
    simplified = operand.simplify({"RefA": True})

    if is_evaluable(expected):
        assert str(simplified) == str(expected)
    else:
        assert simplified == expected


@pytest.mark.parametrize(
    "operands, expected",
    [
        (
            [Value(True), Value(False)],
            'Nor([Value(True), Value(False)], symbol="NOR", not_symbol="NOT")',
        ),
    ],
)
def test___repr__(operands, expected):
    assert repr(Nor(operands)) == expected
