# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest
from illogical.evaluable import is_evaluable

from illogical.expression.logical.nor import Nor
from illogical.expression.logical.logical import InvalidLogicalExpression
from illogical.expression.logical.not_exp import Not
from illogical.operand.reference import Reference
from illogical.operand.value import Value

class TestNor(unittest.TestCase):
    def test_constructor(self):
        tests = [
            ([]),
            ([Value(True)]),
        ]

        for operands in tests:
            with self.assertRaises(InvalidLogicalExpression):
                Nor(operands)

    def test_evaluate(self):
        tests = [
            # Truthy
            ([Value(False), Value(False)], True),
            ([Value(False), Value(False), Value(False)], True),
            # Falsy
            ([Value(True), Value(True)], False),
            ([Value(True), Value(False)], False),
            ([Value(False), Value(True)], False)
        ]

        for operands, expected in tests:
            operand = Nor(operands)
            self.assertIs(operand.evaluate({}), expected)

    def test_simplify(self):
        tests = [
            ([Value(False), Value(False)], True),
            ([Value(True), Value(True)], False),
            ([Value(True), Value(False)], False),
            ([Reference("RefA"), Value(False)], False),
            ([Reference("Missing"), Value(True)], False),
            ([Reference("Missing"), Value(False)], Not(Reference("Missing"))),
            (
                [Reference("Missing"), Reference("Missing")],
                Nor([Reference("Missing"), Reference("Missing")])
            ),
        ]

        for operands, expected in tests:
            operand = Nor(operands)
            simplified = operand.simplify({ "RefA": True })

            if is_evaluable(expected):
                self.assertEqual(str(simplified), str(expected))
            else:
                self.assertEqual(simplified, expected)

if __name__ == '__main__':
    unittest.main()
