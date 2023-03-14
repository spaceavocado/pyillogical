# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.expression.comparison.none import Non
from illogical.operand.reference import Reference
from illogical.operand.value import Value


class TestNone(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            # Truthy
            (Reference("Missing"), True),
            # Falsy
            (Value(1), False),
            (Value(1.1), False),
            (Value("1"), False),
            (Value(True), False),
            (Value(False), False),
        ]

        for operand, expected in tests:
            operand = Non(operand)
            self.assertIs(operand.evaluate({}), expected)

if __name__ == '__main__':
    unittest.main()
