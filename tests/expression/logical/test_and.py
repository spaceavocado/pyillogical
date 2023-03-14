# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.evaluable import is_evaluable
from illogical.expression.logical.and_exp import And
from illogical.expression.logical.logical import InvalidLogicalExpression
from illogical.operand.reference import Reference
from illogical.operand.value import Value


class TestAnd(unittest.TestCase):
    def test_constructor(self):
        tests = [
            ([]),
            ([Value(True)]),
        ]

        for operands in tests:
            with self.assertRaises(InvalidLogicalExpression):
                And(operands)

    def test_evaluate(self):
        tests = [
            # Truthy
            ([Value(True), Value(True)], True),
            ([Value(True), Value(True), Value(True)], True),
            # Falsy
            ([Value(True), Value(False)], False),
            ([Value(False), Value(True)], False),
            ([Value(False), Value(False)], False),
        ]

        for operands, expected in tests:
            operand = And(operands)
            self.assertIs(operand.evaluate({}), expected)

    def test_simplify(self):
        tests = [
            ([Value(True), Value(True)], True),
            ([Value(True), Value(False)], False),
            ([Reference("RefA"), Value(True)], True),
            ([Reference("Missing"), Value(True)], Reference("Missing")),
            (
                [Reference("Missing"), Reference("Missing")],
                And([Reference("Missing"), Reference("Missing")]),
            ),
        ]

        for operands, expected in tests:
            operand = And(operands)
            simplified = operand.simplify({"RefA": True})

            if is_evaluable(expected):
                self.assertEqual(str(simplified), str(expected))
            else:
                self.assertEqual(simplified, expected)


if __name__ == "__main__":
    unittest.main()
