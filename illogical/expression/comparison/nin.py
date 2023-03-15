# pylint: disable=locally-disabled, duplicate-code

"""Not in comparison expression."""

from illogical.evaluable import Evaluable, Evaluated
from illogical.expression.comparison.comparison import Comparison


class Nin(Comparison):
    """Not in comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable, symbol="NOT IN") -> None:
        super().__init__("<not in>", symbol, self.compare, left, right)

    def compare(self, left: Evaluated, right: Evaluated) -> bool:
        """Compare evaluated values."""

        left_is_iterable = isinstance(left, (list, set, tuple))
        right_is_iterable = isinstance(right, (list, set, tuple))

        if (left_is_iterable and right_is_iterable) or (
            not left_is_iterable and not right_is_iterable
        ):
            return True

        if left_is_iterable:
            return right not in left

        return left not in right

    def __repr__(self) -> str:
        return f"Nin({repr(self.operands[0])}, {repr(self.operands[1])})"
