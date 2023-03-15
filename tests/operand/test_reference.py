# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring
# pylint: disable=locally-disabled, missing-function-docstring

import pytest

from illogical.evaluable import flatten_context, is_evaluable
from illogical.operand.reference import (
    DataType,
    Reference,
    context_lookup,
    default_serialize_from,
    default_serialize_to,
    evaluate,
    get_data_type,
    is_ignored_path,
    to_boolean,
    to_float,
    to_int,
    to_number,
    to_string,
    trim_data_type,
)


@pytest.fixture(scope="module")
def example_context():
    return flatten_context(
        {
            "refA": 1,
            "refB": {
                "refB1": 2,
                "refB2": "refB1",
                "refB3": True,
            },
            "refC": "refB1",
            "refD": "refB2",
            "refE": [1, [2, 3, 4]],
            "refF": "A",
            "refG": "1",
            "refH": "1.1",
        }
    )


@pytest.mark.parametrize(
    "address, expected",
    [
        ("", None),
        ("ref", None),
        ("$ref", "ref"),
    ],
)
def test_default_serialize_from(address, expected):
    assert default_serialize_from(address) == expected


@pytest.mark.parametrize(
    "operand, expected",
    [
        ("ref", "$ref"),
    ],
)
def test_default_serialize_to(operand, expected):
    assert default_serialize_to(operand) == expected


@pytest.mark.parametrize(
    "address, expected",
    [
        ("ref", DataType.UNDEFINED),
        ("ref.(X)", DataType.UNDEFINED),
        ("ref.(Bogus)", DataType.UNDEFINED),
        ("ref.(String)", DataType.STRING),
        ("ref.(Number)", DataType.NUMBER),
        ("ref.(Integer)", DataType.INTEGER),
        ("ref.(Float)", DataType.FLOAT),
        ("ref.(Boolean)", DataType.BOOLEAN),
    ],
)
def test_get_data_type(address, expected):
    assert get_data_type(address) == expected


@pytest.mark.parametrize(
    "path, ignored_paths, ignored_path_rx, expected",
    [
        ("path", None, None, False),
        ("ignored", ["ignored"], None, True),
        ("not", ["ignored"], None, False),
        ("refC", None, [r"^ref"], True),
        ("refC.(Number)", None, [r"^ref"], True),
    ],
)
def test_is_ignored_path(path, ignored_paths, ignored_path_rx, expected):
    assert is_ignored_path(path, ignored_paths, ignored_path_rx) == expected


@pytest.mark.parametrize(
    "address, expected",
    [
        ("ref", "ref"),
        ("ref.(X)", "ref.(X)"),
        ("ref.(String)", "ref"),
        ("ref.(Nonsense)", "ref"),
    ],
)
def test_trim_data_type(address, expected):
    assert trim_data_type(address) == expected


@pytest.mark.parametrize(
    "val, expected",
    [
        (1, 1),
        ("1", 1),
        ("1.1", 1.1),
        (True, 1),
        (False, 0),
        ([], []),
    ],
)
def test_to_number(val, expected):
    assert to_number(val) == expected


@pytest.mark.parametrize(
    "val, expected",
    [
        (1, 1),
        (1.1, 1),
        ("1", 1),
        ("1.1", 1),
        ("1.9", 1),
        (True, 1),
        (False, 0),
        ([], []),
    ],
)
def test_to_int(val, expected):
    assert to_int(val) == expected


@pytest.mark.parametrize(
    "val, expected",
    [
        (1, 1.0),
        (1.1, 1.1),
        ("1", 1.0),
        ("1.1", 1.1),
        ("1.9", 1.9),
        (True, True),
        ([], []),
    ],
)
def test_to_float(val, expected):
    assert to_float(val) == expected


@pytest.mark.parametrize(
    "val, expected",
    [
        (1, "1"),
        (1.1, "1.1"),
        ("1", "1"),
        (True, "true"),
    ],
)
def test_to_string(val, expected):
    assert to_string(val) == expected


@pytest.mark.parametrize(
    "val, expected",
    [
        (True, True),
        (False, False),
        ("true", True),
        ("false", False),
        ("True", True),
        ("False", False),
        ("1", True),
        ("0", False),
        (1, True),
        (0, False),
        ([], False),
    ],
)
def test_to_boolean(val, expected):
    assert to_boolean(val) == expected


@pytest.mark.parametrize(
    "path, expected_path, expected_value",
    [
        ("UNDEFINED", "UNDEFINED", None),
        ("refA", "refA", 1),
        ("refB.refB1", "refB.refB1", 2),
        ("refB.{refC}", "refB.refB1", 2),
        ("refB.{UNDEFINED}", "refB.{UNDEFINED}", None),
        ("refB.{refB.refB2}", "refB.refB1", 2),
        ("refB.{refB.{refD}}", "refB.refB1", 2),
        ("refE[0]", "refE[0]", 1),
        ("refE[2]", "refE[2]", None),
        ("refE[1][0]", "refE[1][0]", 2),
        ("refE[1][3]", "refE[1][3]", None),
        ("refE[{refA}][0]", "refE[1][0]", 2),
        ("refE[{refA}][{refB.refB1}]", "refE[1][2]", 4),
        ("ref{refF}", "refA", 1),
        ("ref{UNDEFINED}", "ref{UNDEFINED}", None),
    ],
)
def test_context_lookup(path, expected_path, expected_value, example_context):
    path, value = context_lookup(example_context, path)

    assert path == expected_path
    assert value == expected_value


@pytest.mark.parametrize(
    "path, data_type, expected",
    [
        ("refA", DataType.INTEGER, 1),
        ("refA", DataType.STRING, "1"),
        ("refG", DataType.NUMBER, 1),
        ("refH", DataType.FLOAT, 1.1),
        ("refB.refB3", DataType.STRING, "true"),
        ("refB.refB3", DataType.BOOLEAN, True),
        ("refB.refB3", DataType.NUMBER, 1),
        ("refJ", DataType.UNDEFINED, None),
    ],
)
def test_evaluate(path, data_type, expected, example_context):
    _, result = evaluate(example_context, path, data_type)

    assert result == expected


def test_evaluate_operand(example_context):
    assert Reference("refA").evaluate(example_context) == 1


@pytest.mark.parametrize(
    "address, expected",
    [
        ("refA", "$refA"),
        ("refA.(Number)", "$refA.(Number)"),
    ],
)
def test_serialize(address, expected):
    assert Reference(address).serialize() == expected


@pytest.mark.parametrize(
    "address, expected ",
    [
        ("refJ", Reference("refJ")),
        ("ignored", None),
        ("refA", 1),
        ("refB.{refJ}", Reference("refB.{refJ}")),
        ("refC.{refJ}", None),
    ],
)
def test_simplify(address, expected, example_context):
    operand = Reference(address, default_serialize_to, ["ignored"], [r"^refC"])
    simplified = operand.simplify(example_context)

    if is_evaluable(expected):
        assert str(simplified) == str(expected)
    else:
        assert simplified == expected


@pytest.mark.parametrize(
    "address, expected",
    [
        ("refA", "{refA}"),
        ("refA.(Number)", "{refA.(Number)}"),
    ],
)
def test___srt__(address, expected):
    assert str(Reference(address)) == expected


@pytest.mark.parametrize(
    "address, expected",
    [
        ("refA", 'Reference("refA")'),
        ('re"f"A', r'Reference("re\"f\"A")'),
        ('re\\"f"A', r'Reference("re\"f\"A")'),
        ("refA.(Number)", 'Reference("refA.(Number)")'),
    ],
)
def test___repr__(address, expected):
    assert repr(Reference(address)) == expected
