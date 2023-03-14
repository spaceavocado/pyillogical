# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.expression.comparison.nin import Nin
from illogical.operand.collection import Collection
from illogical.operand.value import Value


class TestNin(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            # Truthy
            (Value(0), Collection([Value(1)]), True),
            (Collection([Value(1)]), Value(0), True),
            (Value("0"), Collection([Value("1")]), True),
            (Value(False), Collection([Value(True)]), True),
            (Value(1.0), Collection([Value(1.1)]), True),
            (Value(1), Value(1), True),
            (Collection([Value(1)]), Collection([Value(1)]), True),
            (Value(1), Collection([Value("1")]), True),
            # Falsy
            (Value(1), Collection([Value(1)]), False),
            (Collection([Value(1)]), Value(1), False),
        ]

        for left, right, expected in tests:
            operand = Nin(left, right)
            self.assertIs(operand.evaluate({}), expected)

if __name__ == '__main__':
    unittest.main()
