# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.evaluable import is_evaluable
from illogical.operand.collection import (
    Collection,
    InvalidCollection,
    escape_operator,
    should_be_escaped,
)
from illogical.operand.reference import Reference
from illogical.operand.value import Value


@pytest.mark.parametrize(
    "operands, expected",
    [([], InvalidCollection)],
)
def test_constructor(operands, expected):
    with pytest.raises(expected):
        Collection(operands)


@pytest.mark.parametrize(
    "subject, expected",
    [
        ("==", True),
        ("!=", False),
        (None, False),
        (True, False),
    ],
)
def test_should_be_escaped(subject, expected):
    assert should_be_escaped(subject, ("==",)) == expected


@pytest.mark.parametrize(
    "operator, escape_character, expected",
    [
        ("==", "\\", "\\=="),
        ("==", "g", "g=="),
    ],
)
def test_escape_operator(operator, escape_character, expected):
    assert escape_operator(operator, escape_character) == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        ([Value(1)], [1]),
        ([Value("1")], ["1"]),
        ([Value(True)], [True]),
        ([Reference("RefA")], ["A"]),
        ([Value(1), Reference("RefA")], [1, "A"]),
    ],
)
def test_evaluate(items, expected):
    assert Collection(items).evaluate({"RefA": "A"}) == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        ([Value(1)], [1]),
        ([Value("1")], ["1"]),
        ([Value(True)], [True]),
        ([Reference("RefA")], ["$RefA"]),
        ([Value(1), Reference("RefA")], [1, "$RefA"]),
        ([Value("=="), Value(1), Value(1)], ["\\==", 1, 1]),
        ([Value("!="), Value(1), Value(1)], ["!=", 1, 1]),
    ],
)
def test_serialize(items, expected):
    assert Collection(items, escaped_operators=("==",)).serialize() == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        ([Reference("RefB")], Collection([Reference("RefB")])),
        ([Reference("RefA")], ["A"]),
        ([Value(1), Reference("RefA")], [1, "A"]),
        (
            [Reference("RefA"), Reference("RefB")],
            Collection([Reference("RefA"), Reference("RefB")]),
        ),
    ],
)
def test_simplify(items, expected):
    simplified = Collection(items).simplify({"RefA": "A"})

    if is_evaluable(simplified):
        assert str(simplified) == str(expected)
    else:
        assert simplified == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        ([Value(1)], "[1]"),
        ([Value("1")], '["1"]'),
        ([Value(True)], "[true]"),
        ([Reference("RefA")], "[{RefA}]"),
        ([Value(1), Reference("RefA")], "[1, {RefA}]"),
    ],
)
def test___str__(items, expected):
    assert str(Collection(items)) == expected


@pytest.mark.parametrize(
    "items, expected",
    [
        ([Value(1)], "Collection([Value(1)])"),
        ([Reference("RefA")], 'Collection([Reference("RefA")])'),
        ([Value(1), Reference("RefA")], 'Collection([Value(1), Reference("RefA")])'),
    ],
)
def test___repr__(items, expected):
    assert repr(Collection(items)) == expected
