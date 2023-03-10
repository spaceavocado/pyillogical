# pylint: disable=locally-disabled, duplicate-code

"""Overlap comparison expression."""

from illogical.evaluable import Evaluable, Evaluated, Kind
from illogical.expression.comparison.comparison import Comparison

KIND = Kind('Overlap')

class Overlap(Comparison):
    """Overlap comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable) -> None:
        super().__init__(
            "<overlaps>",
            KIND,
            self.compare,
            left,
            right
        )

    def compare(self, left: Evaluated, right: Evaluated) -> bool:
        """Compare evaluated values."""

        left_is_iterable = isinstance(left, (list, set, tuple))
        right_is_iterable = isinstance(right, (list, set, tuple))

        if (not left_is_iterable or not right_is_iterable):
            return False

        for i in left:
            for j in right:
                if i is j:
                    return True

        return False
