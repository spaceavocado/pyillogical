# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.expression.comparison.ne import Ne
from illogical.operand.collection import Collection
from illogical.operand.value import Value


class TestNe(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            # Same types
            (Value(1), Value(0), True),
            (Value(1), Value(1), False),
            (Value(1.1), Value(1.0), True),
            (Value(1.1), Value(1.1), False),
            (Value("1"), Value("2"), True),
            (Value("1"), Value("1"), False),
            (Value(True), Value(False), True),
            (Value(True), Value(True), False),
            # Diff types
            (Value(1), Value(1.1), True),
            (Value(1), Value("1"), True),
            (Value(1), Value(True), True),
            (Value(1.1), Value("1"), True),
            (Value(1.1), Value(True), True),
            (Value("1"), Value(True), True),
            # Collection
            (Collection([Value(1)]), Collection([Value(1)]), True),
            (Value(1), Collection([Value(1)]), True),
        ]

        for left, right, expected in tests:
            operand = Ne(left, right)
            self.assertIs(operand.evaluate({}), expected)


if __name__ == "__main__":
    unittest.main()
