"""Not in comparison expression."""

from illogical.evaluable import Evaluable, Evaluated, Kind
from illogical.expression.comparison.comparison import Comparison

KIND = Kind('Not in')

class Nin(Comparison):
    """Not in comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable) -> None:
        super().__init__(
            "<not in>",
            KIND,
            self.compare,
            left,
            right
        )

    def compare(self, left: Evaluated, right: Evaluated) -> bool:
        """Compare evaluated values."""

        left_is_iterable = isinstance(left, (list, set, tuple))
        right_is_iterable = isinstance(right, (list, set, tuple))

        if (left_is_iterable and right_is_iterable) or \
            (not left_is_iterable and not right_is_iterable):
            return True

        if left_is_iterable:
            return not right in left

        return not left in right
