# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest
from illogical.evaluable import is_evaluable
from illogical.expression.logical.nor import Nor

from illogical.expression.logical.xor import Xor
from illogical.expression.logical.logical import InvalidLogicalExpression
from illogical.expression.logical.not_exp import Not
from illogical.operand.reference import Reference
from illogical.operand.value import Value

class TestXor(unittest.TestCase):
    def test_constructor(self):
        tests = [
            ([]),
            ([Value(True)]),
        ]

        for operands in tests:
            with self.assertRaises(InvalidLogicalExpression):
                Xor(*operands)

    def test_evaluate(self):
        tests = [
            # Truthy
            ([Value(True), Value(False)], True),
            ([Value(False), Value(True)], True),
            ([Value(False), Value(True), Value(False)], True),
            # Falsy
            ([Value(True), Value(True)], False),
            ([Value(False), Value(False)], False),
            ([Value(False), Value(True), Value(True)], False),
        ]

        for operands, expected in tests:
            operand = Xor(*operands)
            self.assertIs(operand.evaluate({}), expected)

    def test_simplify(self):
        tests = [
            ([Value(False), Value(False)], False),
            ([Reference("RefA"), Value(True)], False),
            (
                [Reference("Missing"), Value(True), Reference("Missing")],
                Nor(Reference("Missing"), Reference("Missing"))
            ),
            (
                [Reference("Missing"), Value(True), Value(False)],
                Not(Reference("Missing"))
            ),
            ([Reference("RefA"), Reference("RefA"), Value(True)], False),
            ([Value(False), Reference("Missing")], Reference("Missing")),
            (
                [Reference("Missing"), Reference("Missing")],
                Xor(Reference("Missing"), Reference("Missing"))
            ),
        ]

        for operands, expected in tests:
            operand = Xor(*operands)
            simplified = operand.simplify({ "RefA": True })

            if is_evaluable(expected):
                self.assertEqual(str(simplified), str(expected))
            else:
                self.assertEqual(simplified, expected)

if __name__ == '__main__':
    unittest.main()
