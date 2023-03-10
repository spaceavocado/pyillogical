# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.expression.comparison.overlap import Overlap
from illogical.operand.collection import Collection
from illogical.operand.value import Value

class TestEq(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            # Truthy
            (Collection([Value(1)]), Collection([Value(1)]), True),
            (Collection([Value(1), Value(2)]), Collection([Value(1), Value(3)]), True),
            (Collection([Value(3), Value(2)]), Collection([Value(1), Value(2), Value(3)]), True),
            (Collection([Value("1")]), Collection([Value("1")]), True),
            (Collection([Value(True)]), Collection([Value(True)]), True),
            (Collection([Value(1.1)]), Collection([Value(1.1)]), True),
            # Falsy
            (Value(1), Collection([Value(1)]), False),
            (Collection([Value(1)]), Value(1), False),
            (Value(1), Value(1), False),
            (Collection([Value(1)]), Collection([Value(2)]), False),
        ]

        for left, right, expected in tests:
            operand = Overlap(left, right)
            self.assertIs(operand.evaluate({}), expected)

if __name__ == '__main__':
    unittest.main()
