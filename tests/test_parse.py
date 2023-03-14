# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.evaluable import is_evaluable
from illogical.expression.comparison.eq import Eq
from illogical.expression.comparison.ge import Ge
from illogical.expression.comparison.gt import Gt
from illogical.expression.comparison.in_exp import In
from illogical.expression.comparison.le import Le
from illogical.expression.comparison.lt import Lt
from illogical.expression.comparison.ne import Ne
from illogical.expression.comparison.nin import Nin
from illogical.expression.comparison.none import Non
from illogical.expression.comparison.prefix import Prefix
from illogical.expression.comparison.present import Present
from illogical.expression.comparison.suffix import Suffix
from illogical.expression.logical.and_exp import And
from illogical.expression.logical.nor import Nor
from illogical.expression.logical.not_exp import Not
from illogical.expression.logical.or_exp import Or
from illogical.expression.logical.xor import Xor
from illogical.operand.collection import Collection
from illogical.operand.reference import (
    Reference,
    default_serialize_from,
    default_serialize_to,
)
from illogical.operand.value import Value
from illogical.parser.parse import (
    AND,
    DEFAULT_ESCAPE_CHARACTER,
    DEFAULT_OPERATOR_MAPPING,
    EQ,
    GE,
    GT,
    IN,
    LE,
    LT,
    NE,
    NIN,
    NONE,
    NOR,
    NOT,
    OR,
    PREFIX,
    PRESENT,
    SUFFIX,
    XOR,
    UnexpectedExpressionInput,
    UnexpectedOperand,
    is_escaped,
    parse,
    to_reference_address,
)


def address(val: str) -> str:
    return default_serialize_to(val)


class TestParse(unittest.TestCase):
    def test_is_escaped(self):
        tests = [
            ("\\expected", "\\", True),
            ("unexpected", "\\", False),
            ("\\expected", "", False),
        ]

        for val, escape_character, expected in tests:
            self.assertEqual(is_escaped(val, escape_character), expected)

    def test_to_reference_address(self):
        tests = [
            ("$expected", default_serialize_from, "expected"),
            (
                "__expected",
                lambda ref: ref[2:] if ref.startswith("__") else None,
                "expected",
            ),
            ("expected", lambda ref: ref[2:] if ref.startswith("__") else None, None),
            ("unexpected", default_serialize_from, None),
            (1, default_serialize_from, None),
        ]

        for reference, reference_from, expected in tests:
            self.assertEqual(to_reference_address(reference, reference_from), expected)

    def test_value(self):
        tests = [
            (1, Value(1)),
            (1.1, Value(1.1)),
            ("val", Value("val")),
            (True, Value(True)),
        ]

        for expression, expected in tests:
            res = parse(expression)
            self.assertTrue(is_evaluable(res))
            self.assertEqual(str(res), str(expected))

    def test_reference(self):
        tests = [
            (address("path"), Reference("path")),
        ]

        for expression, expected in tests:
            res = parse(expression)
            self.assertTrue(is_evaluable(res))
            self.assertEqual(str(res), str(expected))

    def test_collection(self):
        tests = [
            ([1], Collection([Value(1)])),
            (["val"], Collection([Value("val")])),
            (["val1", "val2"], Collection([Value("val1"), Value("val2")])),
            ([True], Collection([Value(True)])),
            ([address("ref")], Collection([Reference("ref")])),
            (
                [1, "val", True, address("ref")],
                Collection([Value(1), Value("val"), Value(True), Reference("ref")]),
            ),
            # escaped
            (
                [f"{DEFAULT_ESCAPE_CHARACTER}{DEFAULT_OPERATOR_MAPPING[AND]}", 1],
                Collection([Value(DEFAULT_OPERATOR_MAPPING[AND]), Value(1)]),
            ),
        ]

        for expression, expected in tests:
            res = parse(expression)
            self.assertTrue(is_evaluable(res))
            self.assertEqual(str(res), str(expected))

    def test_comparison(self):
        tests = [
            ([DEFAULT_OPERATOR_MAPPING[EQ], 1, 1], Eq(Value(1), Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[NE], 1, 1], Ne(Value(1), Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[GT], 1, 1], Gt(Value(1), Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[GE], 1, 1], Ge(Value(1), Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[LT], 1, 1], Lt(Value(1), Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[LE], 1, 1], Le(Value(1), Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[IN], 1, 1], In(Value(1), Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[NIN], 1, 1], Nin(Value(1), Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[NONE], 1, 1], Non(Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[PRESENT], 1, 1], Present(Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[SUFFIX], 1, 1], Suffix(Value(1), Value(1))),
            ([DEFAULT_OPERATOR_MAPPING[PREFIX], 1, 1], Prefix(Value(1), Value(1))),
        ]

        for expression, expected in tests:
            res = parse(expression)
            self.assertTrue(is_evaluable(res))
            self.assertEqual(str(res), str(expected))

    def test_logical(self):
        tests = [
            (
                [DEFAULT_OPERATOR_MAPPING[AND], True, True],
                And([Value(True), Value(True)]),
            ),
            (
                [DEFAULT_OPERATOR_MAPPING[OR], True, True],
                Or([Value(True), Value(True)]),
            ),
            (
                [DEFAULT_OPERATOR_MAPPING[NOR], True, True],
                Nor([Value(True), Value(True)]),
            ),
            (
                [DEFAULT_OPERATOR_MAPPING[XOR], True, True],
                Xor([Value(True), Value(True)]),
            ),
            ([DEFAULT_OPERATOR_MAPPING[NOT], True], Not(Value(True))),
        ]

        for expression, expected in tests:
            res = parse(expression)
            self.assertTrue(is_evaluable(res))
            self.assertEqual(str(res), str(expected))

    def test_invalid(self):
        tests = [
            (None, UnexpectedExpressionInput),
            ([], UnexpectedOperand),
            ([lambda: True], UnexpectedOperand),
            (["val1", lambda: True], UnexpectedOperand),
        ]

        for expression, expected in tests:
            with self.assertRaises(expected):
                parse(expression)


if __name__ == "__main__":
    unittest.main()
