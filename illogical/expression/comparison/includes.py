"""In comparison expression."""

from illogical.evaluable import Evaluable, Evaluated, Kind
from illogical.expression.comparison.comparison import Comparison

KIND = Kind('In')

class In(Comparison):
    """In comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable) -> None:
        super().__init__(
            "<in>",
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
            return False

        if left_is_iterable:
            return right in left

        return left in right
