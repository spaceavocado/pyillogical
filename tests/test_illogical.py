# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.evaluable import is_evaluable
from illogical.expression.comparison.eq import Eq
from illogical.expression.logical.and_exp import And
from illogical.illogical import Illogical
from illogical.operand.collection import Collection
from illogical.operand.reference import Reference, default_serialize_to
from illogical.operand.value import Value
from illogical.parser.parse import AND, DEFAULT_OPERATOR_MAPPING, EQ, Options


def address(val: str) -> str:
    return default_serialize_to(val)


class TestIllogical(unittest.TestCase):
    def test_parse(self):
        tests = [
            (1, Value(1)),
            (address("path"), Reference("path")),
            ([1], Collection([Value(1)])),
            ([DEFAULT_OPERATOR_MAPPING[EQ], 1, 1], Eq(Value(1), Value(1))),
            (
                [DEFAULT_OPERATOR_MAPPING[AND], True, True],
                And([Value(True), Value(True)]),
            ),
        ]

        for expression, expected in tests:
            res = Illogical().parse(expression)
            self.assertTrue(is_evaluable(res))
            self.assertEqual(str(res), str(expected))

    def test_evaluate(self):
        tests = [
            (1, 1),
            (address("path"), "value"),
            ([1], [1]),
            ([DEFAULT_OPERATOR_MAPPING[EQ], 1, 1], True),
            ([DEFAULT_OPERATOR_MAPPING[AND], True, False], False),
        ]

        for expression, expected in tests:
            self.assertEqual(
                Illogical().evaluate(expression, {"path": "value"}), expected
            )

    def test_simplify(self):
        tests = [
            (1, 1),
            (address("path"), "value"),
            (address("nested.inner"), 2),
            (address("list[1]"), 3),
            (address("missing"), Reference("missing")),
            ([1], [1]),
            ([DEFAULT_OPERATOR_MAPPING[EQ], 1, 1], True),
            ([DEFAULT_OPERATOR_MAPPING[AND], True, True], True),
            (
                [DEFAULT_OPERATOR_MAPPING[AND], True, address("missing")],
                Reference("missing"),
            ),
        ]

        for expression, expected in tests:
            res = Illogical().simplify(
                expression, {"path": "value", "nested": {"inner": 2}, "list": [1, 3]}
            )

            if is_evaluable(expected):
                self.assertEqual(str(res), str(expected))
            else:
                self.assertEqual(res, expected)

    def test_statement(self):
        tests = [
            (1, "1"),
            (True, "true"),
            ("val", '"val"'),
            ("$refA", "{refA}"),
            (["==", 1, 1], "(1 == 1)"),
            (["==", "$refA", "resolvedA"], '({refA} == "resolvedA")'),
            (["AND", ["==", 1, 1], ["!=", 2, 1]], "((1 == 1) AND (2 != 1))"),
        ]

        for expression, expected in tests:
            self.assertEqual(Illogical().statement(expression), expected)

    def test_operator_mapping(self):
        tests = [
            (["IS", 1, 1], True),
            (["IS", 1, 2], False),
        ]

        operator_mapping = DEFAULT_OPERATOR_MAPPING.copy()
        operator_mapping[EQ] = "IS"

        for expression, expected in tests:
            self.assertEqual(
                Illogical(Options(operator_mapping=operator_mapping)).evaluate(
                    expression, {}
                ),
                expected,
            )

    def test_escape_character(self):
        tests = [
            (["*AND", 1, 1], Collection([Value("AND"), Value(1), Value(1)])),
        ]

        for expression, expected in tests:
            self.assertEqual(
                str(Illogical(Options(escape_character="*")).parse(expression)),
                str(expected),
            )


if __name__ == "__main__":
    unittest.main()
