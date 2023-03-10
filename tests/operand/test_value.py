# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest

from illogical.operand.value import Value

class TestValue(unittest.TestCase):
    def test_evaluate(self):
        tests = [
            (1, 1),
            (1.1, 1.1),
            ("val", "val"),
            (True, True),
            (False, False),
        ]

        for arg, expected in tests:
            operand = Value(arg)
            self.assertIs(operand.evaluate({}), expected)

    def test_serialize(self):
        tests = [
            (1, 1),
            (1.1, 1.1),
            ("val", "val"),
            (True, True),
            (False, False),
        ]

        for arg, expected in tests:
            operand = Value(arg)
            self.assertIs(operand.serialize(), expected)

    def test_simplify(self):
        tests = [
            (1, 1),
            (1.1, 1.1),
            ("val", "val"),
            (True, True),
            (False, False),
        ]

        for arg, expected in tests:
            operand = Value(arg)
            self.assertIs(operand.simplify({}), expected)

    def test___str__(self):
        tests = [
            (1, "1"),
            (1.1, "1.1"),
            ("val", '"val"'),
            (True, "True"),
            (False, "False"),
        ]

        for arg, expected in tests:
            operand = Value(arg)
            self.assertEqual(str(operand), expected)

if __name__ == '__main__':
    unittest.main()
