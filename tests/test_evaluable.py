# pylint: disable=locally-disabled, missing-module-docstring, missing-class-docstring, missing-function-docstring

import unittest
from illogical.evaluable import flatten_context

class TestReference(unittest.TestCase):
    def test_flatten_context(self):
        tests = [
            (
                {"a": 1},
                {"a": 1}
            ),
		    (
                {"a": 1, "b": {"c": 5, "d": True}},
                {"a": 1, "b.c": 5, "b.d": True}
            ),
		    (
                {"a": 1, "b": [1, 2, 3]},
                {"a": 1, "b[0]": 1, "b[1]": 2, "b[2]": 3}
            ),
		    (
                {"a": 1, "b": [1, 2, {"c": 5, "d": True, "e": lambda x: x}]},
                {"a": 1, "b[0]": 1, "b[1]": 2, "b[2].c": 5, "b[2].d": True}
            ),
        ]

        for context, expected in tests:
            self.assertEqual(flatten_context(context), expected)

if __name__ == '__main__':
    unittest.main()
