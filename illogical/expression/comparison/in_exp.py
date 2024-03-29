"""In comparison expression."""

from illogical.evaluable import Evaluable, Evaluated
from illogical.expression.comparison.comparison import Comparison


class In(Comparison):
    """In comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable, symbol="IN") -> None:
        super().__init__("<in>", symbol, self.compare, left, right)

    def compare(self, left: Evaluated, right: Evaluated) -> bool:
        """Compare evaluated values."""

        left_is_iterable = isinstance(left, (list, set, tuple))
        right_is_iterable = isinstance(right, (list, set, tuple))

        if (left_is_iterable and right_is_iterable) or (
            not left_is_iterable and not right_is_iterable
        ):
            return False

        if left_is_iterable:
            return right in left

        return left in right

    def __repr__(self) -> str:
        return f"In({repr(self.operands[0])}, {repr(self.operands[1])})"
