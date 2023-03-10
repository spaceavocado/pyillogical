# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.expression.comparison.prefix import Prefix
from illogical.operand.collection import Collection
from illogical.operand.value import Value

class TestEq(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            # Truthy
            (Value("bo"), Value("bogus"), True),
            # Falsy
            (Value("bo"), Value("something"), False),
            # Diff types
            (Value(1), Value(1.1), False),
            (Value(1), Value("1"), False),
            (Value(1), Value(True), False),
            (Value(1.1), Value("1"), False),
            (Value(1.1), Value(True), False),
            (Value("1"), Value(True), False),
            # Collection
            (Collection([Value(1)]), Collection([Value(1)]), False),
            (Value(1), Collection([Value(1)]), False),
        ]

        for left, right, expected in tests:
            operand = Prefix(left, right)
            self.assertIs(operand.evaluate({}), expected)

if __name__ == '__main__':
    unittest.main()
