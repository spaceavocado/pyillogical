# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.expression.comparison.lt import Lt
from illogical.operand.value import Value

class TestLt(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            # Truthy
            (Value(1), Value(2), True),
            (Value(1.1), Value(1.2), True),
            (Value(1), Value(1.1), True),
            # Falsy
            (Value(1), Value(1), False),
            (Value(1.1), Value(1.1), False),
            (Value(1), Value(0), False),
            (Value(1.1), Value(1.0), False),
            # Non comparable
            (Value("Value"), Value(1), False),
        ]

        for left, right, expected in tests:
            operand = Lt(left, right)
            self.assertIs(operand.evaluate({}), expected)

if __name__ == '__main__':
    unittest.main()
