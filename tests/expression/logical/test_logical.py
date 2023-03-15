# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.evaluable import Kind
from illogical.expression.logical.logical import Logical
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "operator, operands, expected",
    [
        ("->", [Value(1), Value(2)], ["->", 1, 2]),
        ("X", [Value(1)], ["X", 1]),
    ],
)
def test_serialize(operator, operands, expected):
    assert Logical(operator, Kind(operator), *operands).serialize() == expected


@pytest.mark.parametrize(
    "operator, operands, expected",
    [
        ("->", [Value(1), Value("2")], '(1 -> "2")'),
        ("->", [Value(1), Value("2"), Value(1)], '(1 -> "2" -> 1)'),
        ("X", [Value(1)], "(X 1)"),
    ],
)
def test___str__(operator, operands, expected):
    assert str(Logical(operator, Kind(operator), *operands)) == expected
