# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.expression.comparison.eq import Eq
from illogical.operand.collection import Collection
from illogical.operand.value import Value


class TestEq(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            # Same types
            (Value(1), Value(1), True),
            (Value(1.1), Value(1.1), True),
            (Value("1"), Value("1"), True),
            (Value(True), Value(True), True),
            (Value(False), Value(False), True),
            # # Diff types
            (Value(1), Value(1.1), False),
            (Value(1), Value("1"), False),
            (Value(1), Value(True), False),
            (Value(1.1), Value("1"), False),
            (Value(1.1), Value(True), False),
            (Value("1"), Value(True), False),
            # Collections
            (Collection([Value(1)]), Collection([Value(1)]), False),
            (Value(1), Collection([Value(1)]), False),
        ]

        for left, right, expected in tests:
            operand = Eq(left, right)
            self.assertIs(operand.evaluate({}), expected)

if __name__ == '__main__':
    unittest.main()
