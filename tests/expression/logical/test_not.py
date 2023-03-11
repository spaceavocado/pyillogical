# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest
from illogical.evaluable import is_evaluable

from illogical.expression.logical.not_exp import InvalidNotExpression, Not
from illogical.operand.reference import Reference
from illogical.operand.value import Value

class TestNot(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            (Value(True), False),
            (Value(False), True),
        ]

        for operand, expected in tests:
            operand = Not(operand)
            self.assertIs(operand.evaluate({}), expected)

        with self.assertRaises(InvalidNotExpression):
            Not(Value("val")).evaluate({})

    def test_simplify(self):
        tests = [
            (Value(True), False),
            (Value(False), True),
            (Reference("RefA"), False),
            (Reference("Missing"), Not(Reference("Missing"))),
        ]

        for operand, expected in tests:
            operand = Not(operand)
            simplified = operand.simplify({ "RefA": True })

            if is_evaluable(expected):
                self.assertEqual(str(simplified), str(expected))
            else:
                self.assertEqual(simplified, expected)

if __name__ == '__main__':
    unittest.main()
