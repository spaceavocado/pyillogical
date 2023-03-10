# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest
from illogical.evaluable import Evaluable, Kind, is_evaluable

from illogical.expression.comparison.comparison import Comparison
from illogical.operand.reference import Reference
from illogical.operand.value import Value

class TestEq(unittest.TestCase):
    def test_serialize(self):
        tests = [
            ("==", [Value(1), Value(2)], "(1 == 2)"),
            ("<nil>", [Value(1)], "(1 <nil>)"),
        ]

        for operator, operands, expected in tests:
            operand = Comparison(operator, Kind(operator), lambda *_: False, *operands)
            self.assertEqual(str(operand), expected)

    def test_simplify(self):
        class Op(Comparison):
            def __init__(self, left: Evaluable, right: Evaluable) -> None:
                super().__init__(
                    "==",
                    Kind("=="),
                    lambda left, right: left is right,
                    left,
                    right
                )

        tests = [
            ([Value(0), Reference("Missing")], Op(Value(0), Reference("Missing"))),
            ([Reference("Missing"), Value(0)], Op(Reference("Missing"), Value(0))),
            (
                [Reference("Missing"), Reference("Missing")],
                Op(Reference("Missing"), Reference("Missing"))
            ),
            ([Value(0), Value(0)], True),
            ([Value(0), Value(1)], False),
            ([Value("A"), Reference("RefA")], True),
        ]

        for operands, expected in tests:
            operand = Comparison("==", Kind("=="), lambda left, right: left is right, *operands)
            simplified = operand.simplify({ "RefA": "A" })

            if is_evaluable(expected):
                self.assertEqual(str(simplified), str(expected))
            else:
                self.assertEqual(simplified, expected)

    def test___str__(self):
        tests = [
            ("->", [Value(1), Value(2)], ["->", 1, 2]),
            ("X", [Value(1)], ["X", 1]),
        ]

        for operator, operands, expected in tests:
            operand = Comparison(operator, Kind(operator), lambda *_: False, *operands)
            self.assertEqual(operand.serialize(), expected)

if __name__ == '__main__':
    unittest.main()
