# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.evaluable import flatten_context, is_evaluable, is_primitive
from illogical.expression.logical.and_exp import And
from illogical.operand.value import Value


class TestEvaluable(unittest.TestCase):
    def test_is_primitive(self):
        tests = [
            (None, True),
            ("val", True),
            (1, True),
            (1.1, True),
            (True, True),
            (False, True),
            ([], False),
            ((), False),
            ({}, False),
        ]

        for subject, expected in tests:
            self.assertEqual(is_primitive(subject), expected)

    def test_is_evaluable(self):
        tests = [
            (Value(1), True),
            (And([Value(1), Value(1)]), True),
            (None, False),
            ("val", False),
            (1, False),
            (1.1, False),
            (True, False),
            (False, False),
        ]

        for subject, expected in tests:
            self.assertEqual(is_evaluable(subject), expected)

    def test_flatten_context(self):
        tests = [
            ({"a": 1}, {"a": 1}),
            ({"a": 1, "b": {"c": 5, "d": True}}, {"a": 1, "b.c": 5, "b.d": True}),
            ({"a": 1, "b": [1, 2, 3]}, {"a": 1, "b[0]": 1, "b[1]": 2, "b[2]": 3}),
            (
                {"a": 1, "b": [1, 2, {"c": 5, "d": True, "e": lambda x: x}]},
                {"a": 1, "b[0]": 1, "b[1]": 2, "b[2].c": 5, "b[2].d": True},
            ),
        ]

        for context, expected in tests:
            self.assertEqual(flatten_context(context), expected)


if __name__ == "__main__":
    unittest.main()
