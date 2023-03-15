# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.evaluable import Evaluable, Kind, is_evaluable
from illogical.expression.comparison.comparison import Comparison
from illogical.operand.reference import Reference
from illogical.operand.value import Value


class ComparisonMock(Comparison):
    def __init__(self, left: Evaluable, right: Evaluable) -> None:
        super().__init__(
            "==", Kind("=="), lambda left, right: left is right, left, right
        )


@pytest.mark.parametrize(
    "operator, operands, expected",
    [
        ("->", [Value(1), Value(2)], ["->", 1, 2]),
        ("X", [Value(1)], ["X", 1]),
    ],
)
def test_serialize(operator, operands, expected):
    operand = Comparison(operator, Kind(operator), lambda *_: False, *operands)
    assert operand.serialize() == expected


@pytest.mark.parametrize(
    "operands, expected",
    [
        (
            [Value(0), Reference("Missing")],
            ComparisonMock(Value(0), Reference("Missing")),
        ),
        (
            [Reference("Missing"), Value(0)],
            ComparisonMock(Reference("Missing"), Value(0)),
        ),
        (
            [Reference("Missing"), Reference("Missing")],
            ComparisonMock(Reference("Missing"), Reference("Missing")),
        ),
        ([Value(0), Value(0)], True),
        ([Value(0), Value(1)], False),
        ([Value("A"), Reference("RefA")], True),
    ],
)
def test_simplify(operands, expected):
    operand = Comparison("==", Kind("=="), lambda left, right: left is right, *operands)
    simplified = operand.simplify({"RefA": "A"})

    if is_evaluable(expected):
        assert str(simplified) == str(expected)
    else:
        assert simplified == expected


@pytest.mark.parametrize(
    "operator, operands, expected",
    [
        ("==", [Value(1), Value(2)], "(1 == 2)"),
        ("<nil>", [Value(1)], "(1 <nil>)"),
    ],
)
def test___str__(operator, operands, expected):
    operand = Comparison(operator, Kind(operator), lambda *_: False, *operands)

    assert str(operand) == expected
