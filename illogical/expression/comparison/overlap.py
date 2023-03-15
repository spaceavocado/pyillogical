# pylint: disable=locally-disabled, duplicate-code

"""Overlap comparison expression."""

from illogical.evaluable import Evaluable, Evaluated
from illogical.expression.comparison.comparison import Comparison


class Overlap(Comparison):
    """Overlap comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable, symbol="OVERLAP") -> None:
        super().__init__("<overlaps>", symbol, self.compare, left, right)

    def compare(self, left: Evaluated, right: Evaluated) -> bool:
        """Compare evaluated values."""

        left_is_iterable = isinstance(left, (list, set, tuple))
        right_is_iterable = isinstance(right, (list, set, tuple))

        if not left_is_iterable or not right_is_iterable:
            return False

        for i in left:
            for j in right:
                if i is j:
                    return True

        return False

    def __repr__(self) -> str:
        return f"Overlap({repr(self.operands[0])}, {repr(self.operands[1])})"
