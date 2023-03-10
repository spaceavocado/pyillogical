# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest
from illogical.evaluable import is_evaluable

from illogical.operand.collection import Collection, InvalidCollection, should_be_escaped, escape_operator
from illogical.operand.value import Value
from illogical.operand.reference import Reference

class TestCollection(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(InvalidCollection):
            Collection([])

    def test_should_be_escaped(self):
        tests = [
            ("==", True),
            ("!=", False),
            (None, False),
            (True, False),
        ]

        for subject, expected in tests:
            self.assertEqual(should_be_escaped(subject, ("==")), expected)

    def escape_operator(self):
        tests = [
            ("==", "\\=="),
        ]

        for operator, expected in tests:
            self.assertEqual(escape_operator(operator, "\\"), expected)

    def test_evaluate(self):
        context = {
		    "RefA": "A",
	    }

        tests = [
            ([Value(1)], [1]),
            ([Value("1")], ["1"]),
            ([Value(True)], [True]),
            ([Reference("RefA")], ["A"]),
            ([Value(1), Reference("RefA")], [1, "A"]),
            # ({expBinary(eq.New, val(1), val(1)), ref("RefA")}, []any{true, "A"}),
        ]

        for items, expected in tests:
            operand = Collection(items)
            self.assertEqual(operand.evaluate(context), expected)

    def test_serialize(self):
        tests = [
            ([Value(1)], [1]),
            ([Value("1")], ["1"]),
            ([Value(True)], [True]),
            ([Reference("RefA")], ["$RefA"]),
            ([Value(1), Reference("RefA")], [1, "$RefA"]),
            # ({expBinary(eq.New, val(1), val(1)), ref("RefA")}, []any{true, "A"}),
            ([Value("=="), Value(1), Value(1)], ["\\==", 1, 1]),
        ]

        for items, expected in tests:
            operand = Collection(items, "\\", ("=="))
            self.assertEqual(operand.serialize(), expected)

    def test_simplify(self):
        context = {
		    "RefA": "A",
	    }

        tests = [
            ([Reference("RefB")], Collection([Reference("RefB")])),
            ([Reference("RefA")], ["A"]),
            ([Value(1), Reference("RefA")], [1, "A"]),
            (
                [Reference("RefA"), Reference("RefB")],
                Collection([Reference("RefA"), Reference("RefB")])
            ),
        ]

        for items, expected in tests:
            operand = Collection(items)
            simplified = operand.simplify(context)

            if is_evaluable(simplified):
                self.assertEqual(str(simplified), str(expected))
            else:
                self.assertEqual(simplified, expected)

    def test___str__(self):
        tests = [
            ([Value(1)], "[1]"),
            ([Value("1")], "[\"1\"]"),
            ([Value(True)], "[true]"),
            ([Reference("RefA")], "[{RefA}]"),
            ([Value(1), Reference("RefA")], "[1, {RefA}]"),
            # ({expBinary(eq.New, val(1), val(1)), ref("RefA")}, []any{true, "A"}),
        ]

        for items, expected in tests:
            operand = Collection(items)
            self.assertEqual(str(operand), expected)

if __name__ == '__main__':
    unittest.main()
