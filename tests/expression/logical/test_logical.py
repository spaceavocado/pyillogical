# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.evaluable import Kind
from illogical.expression.logical.logical import Logical
from illogical.operand.value import Value


class TestLogical(unittest.TestCase):
    def test_serialize(self):
        tests = [
            ("->", [Value(1), Value(2)], ["->", 1, 2]),
            ("X", [Value(1)], ["X", 1]),
        ]

        for operator, operands, expected in tests:
            operand = Logical(operator, Kind(operator), *operands)
            self.assertEqual(operand.serialize(), expected)

    def test___str__(self):
        tests = [
            ("->", [Value(1), Value("2")], '(1 -> "2")'),
            ("->", [Value(1), Value("2"), Value(1)], '(1 -> "2" -> 1)'),
            ("X", [Value(1)], "(X 1)"),
        ]

        for operator, operands, expected in tests:
            operand = Logical(operator, Kind(operator), *operands)
            self.assertEqual(str(operand), expected)

if __name__ == '__main__':
    unittest.main()
