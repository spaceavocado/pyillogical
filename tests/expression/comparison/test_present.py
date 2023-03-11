# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.expression.comparison.present import Present
from illogical.operand.reference import Reference
from illogical.operand.value import Value

class TestPresent(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            # Truthy
            (Value(1), True),
            (Value(1.1), True),
            (Value("1"), True),
            (Value(True), True),
            (Value(False), True),
            # Falsy
            (Reference("Missing"), False),
        ]

        for operand, expected in tests:
            operand = Present(operand)
            self.assertIs(operand.evaluate({}), expected)

if __name__ == '__main__':
    unittest.main()
