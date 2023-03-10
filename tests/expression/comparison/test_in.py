# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.expression.comparison.includes import In
from illogical.operand.collection import Collection
from illogical.operand.value import Value

class TestEq(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            # Truthy
            (Value(1), Collection([Value(1)]), True),
            (Collection([Value(1)]), Value(1), True),
            (Value("1"), Collection([Value("1")]), True),
            (Value(True), Collection([Value(True)]), True),
            (Value(1.1), Collection([Value(1.1)]), True),
            # Falsy
            (Value(1), Collection([Value(2)]), False),
            (Collection([Value(2)]), Value(1), False),
            (Value(1), Value(1), False),
            (Collection([Value(1)]), Collection([Value(1)]), False),
            (Value(1), Collection([Value("1")]), False),
        ]

        for left, right, expected in tests:
            operand = In(left, right)
            self.assertIs(operand.evaluate({}), expected)

if __name__ == '__main__':
    unittest.main()
