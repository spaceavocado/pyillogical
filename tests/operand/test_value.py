# pylint: disable=locally-disabled, missing-module-docstring, missing-function-docstring

import pytest

from illogical.operand.value import Value


@pytest.mark.parametrize(
    "val, expected",
    [
        (1, 1),
        (1.1, 1.1),
        ("val", "val"),
        (True, True),
        (False, False),
    ],
)
def test_evaluate(val, expected):
    assert Value(val).evaluate({}) == expected


@pytest.mark.parametrize(
    "val, expected",
    [
        (1, 1),
        (1.1, 1.1),
        ("val", "val"),
        (True, True),
        (False, False),
    ],
)
def test_serialize(val, expected):
    assert Value(val).serialize() == expected


@pytest.mark.parametrize(
    "val, expected",
    [
        (1, 1),
        (1.1, 1.1),
        ("val", "val"),
        (True, True),
        (False, False),
    ],
)
def test_simplify(val, expected):
    assert Value(val).simplify({}) == expected


@pytest.mark.parametrize(
    "val, expected",
    [
        (1, "1"),
        (1.1, "1.1"),
        ("val", '"val"'),
        (True, "true"),
        (False, "false"),
    ],
)
def test___str__(val, expected):
    assert str(Value(val)) == expected


@pytest.mark.parametrize(
    "val, expected",
    [
        (1, "Value(1)"),
        (1.1, "Value(1.1)"),
        ("val", 'Value("val")'),
        (True, "Value(True)"),
        (False, "Value(False)"),
    ],
)
def test___repr__(val, expected):
    assert repr(Value(val)) == expected
