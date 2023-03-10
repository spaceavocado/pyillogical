# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest
from illogical.evaluable import is_evaluable

from illogical.expression.logical.or_exp import Or
from illogical.expression.logical.logical import InvalidLogicalExpression
from illogical.operand.reference import Reference
from illogical.operand.value import Value

class TestOr(unittest.TestCase):
    def test_constructor(self):
        tests = [
            ([]),
            ([Value(True)]),
        ]

        for operands in tests:
            with self.assertRaises(InvalidLogicalExpression):
                Or(operands)

    def test_evaluate(self):
        tests = [
            # Truthy
            ([Value(True), Value(True)], True),
            ([Value(True), Value(False)], True),
            ([Value(False), Value(False), Value(True)], True),
            # Falsy
            ([Value(False), Value(False)], False)
        ]

        for operands, expected in tests:
            operand = Or(operands)
            self.assertIs(operand.evaluate({}), expected)

    def test_simplify(self):
        tests = [
            ([Value(True), Value(True)], True),
            ([Value(True), Value(False)], True),
            ([Value(False), Value(False)], False),
            ([Reference("RefA"), Value(False)], True),
            ([Reference("Missing"), Value(False)], Reference("Missing")),
            (
                [Reference("Missing"), Reference("Missing")],
                Or([Reference("Missing"), Reference("Missing")])
            ),
        ]

        for operands, expected in tests:
            operand = Or(operands)
            simplified = operand.simplify({ "RefA": True })

            if is_evaluable(expected):
                self.assertEqual(str(simplified), str(expected))
            else:
                self.assertEqual(simplified, expected)

if __name__ == '__main__':
    unittest.main()
