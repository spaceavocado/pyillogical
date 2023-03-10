# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest
from illogical.evaluable import flatten_context, is_evaluable

from illogical.operand.reference import DataType, Reference, context_lookup, default_serialize_from, default_serialize_to, evaluate, get_data_type, is_ignored_path, to_boolean, to_float, to_int, to_number, to_string, trim_data_type

class TestReference(unittest.TestCase):
    def test_default_serialize_from(self):
        tests = [
            ("", ""),
            ("ref", ""),
            ("$ref", "ref"),
        ]

        for address, expected in tests:
            self.assertEqual(default_serialize_from(address), expected)

    def test_default_serialize_to(self):
        tests = [
            ("ref", "$ref"),
        ]

        for operand, expected in tests:
            self.assertEqual(default_serialize_to(operand), expected)

    def test_get_data_type(self):
        tests = [
            ("ref", DataType.UNDEFINED),
            ("ref.(X)", DataType.UNDEFINED),
            ("ref.(Bogus)", DataType.UNDEFINED),
            ("ref.(String)", DataType.STRING),
            ("ref.(Number)", DataType.NUMBER),
            ("ref.(Integer)", DataType.INTEGER),
            ("ref.(Float)", DataType.FLOAT),
            ("ref.(Boolean)", DataType.BOOLEAN),
        ]

        for address, expected in tests:
            self.assertEqual(get_data_type(address), expected)

    def test_is_ignored_path(self):
        ignored_paths = ["ignored"]
        ignored_path_rx = [r'^refC']

        tests = [
            ("ignored", True),
            ("not", False),
            ("refC", True),
            ("refC.(Number)", True),
        ]

        for path, expected in tests:
            self.assertEqual(is_ignored_path(path, ignored_paths, ignored_path_rx), expected)

        self.assertEqual(is_ignored_path("path", None, None), False)

    def test_trim_data_type(self):
        tests = [
            ("ref", "ref"),
            ("ref.(X)", "ref.(X)"),
            ("ref.(String)", "ref"),
            ("ref.(Nonsense)", "ref"),
        ]

        for address, expected in tests:
            self.assertEqual(trim_data_type(address), expected)

    def test_to_number(self):
        tests = [
            (1, 1),
            ("1", 1),
            ("1.1", 1.1),
            (True, 1),
            (False, 0),
            ([], []),
        ]

        for val, expected in tests:
            self.assertEqual(to_number(val), expected)

    def test_to_int(self):
        tests = [
            (1, 1),
            (1.1, 1),
            ("1", 1),
            ("1.1", 1),
            ("1.9", 1),
            (True, 1),
            (False, 0),
            ([], []),
        ]

        for val, expected in tests:
            self.assertEqual(to_int(val), expected)

    def test_to_float(self):
        tests = [
            (1, 1.0),
            (1.1, 1.1),
            ("1", 1.0),
            ("1.1", 1.1),
            ("1.9", 1.9),
            (True, True),
            ([], []),
        ]

        for val, expected in tests:
            self.assertEqual(to_float(val), expected)

    def test_to_string(self):
        tests = [
            (1, "1"),
            (1.1, "1.1"),
            ("1", "1"),
            (True, "true"),
        ]

        for val, expected in tests:
            self.assertEqual(to_string(val), expected)

    def test_to_boolean(self):
        tests = [
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
        ]

        for val, expected in tests:
            self.assertEqual(to_boolean(val), expected)

    def test_context_lookup(self):
        context = flatten_context({
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
        })

        tests = [
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
        ]

        for path, expected_path, expected_value in tests:
            path, value = context_lookup(context, path)
            self.assertEqual(path, expected_path)
            self.assertEqual(value, expected_value)

    def test_evaluate(self):
        context = flatten_context({
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
        })

        tests = [
            ("refA", DataType.INTEGER, 1),
            ("refA", DataType.STRING, "1"),
            ("refG", DataType.NUMBER, 1),
            ("refH", DataType.FLOAT, 1.1),
            ("refB.refB3", DataType.STRING, "true"),
            ("refB.refB3", DataType.BOOLEAN, True),
            ("refB.refB3", DataType.NUMBER, 1),
            ("refJ", DataType.UNDEFINED, None),
        ]

        for path, data_type, expected in tests:
            self.assertEqual(evaluate(context, path, data_type)[1], expected)

        self.assertEqual(Reference("refA").evaluate(context), 1)

    def test_serialize(self):
        tests = [
            ("refA", "$refA"),
            ("refA.(Number)", "$refA.(Number)"),
        ]

        for address, expected in tests:
            operand = Reference(address)
            self.assertEqual(operand.serialize(), expected)

    def test_simplify(self):
        ignored_paths = ["ignored"]
        ignored_path_rx = [r'^refC']

        context = flatten_context({
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
        })

        tests = [
            ("refJ", Reference("refJ")),
            ("ignored", None),
            ("refA", 1),
            ("refB.{refJ}", Reference("refB.{refJ}")),
            ("refC.{refJ}", None),
        ]

        for address, expected in tests:
            operand = Reference(address, default_serialize_to, ignored_paths, ignored_path_rx)
            simplified = operand.simplify(context)

            if is_evaluable(expected):
                self.assertEqual(str(simplified), str(expected))
            else:
                self.assertEqual(simplified, expected)

    def test___str__(self):
        tests = [
            ("refA", "{refA}"),
            ("refA.(Number)", "{refA.(Number)}"),
        ]

        for address, expected in tests:
            operand = Reference(address)
            self.assertEqual(str(operand), expected)

if __name__ == '__main__':
    unittest.main()
