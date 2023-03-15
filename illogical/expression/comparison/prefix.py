"""Has prefix comparison expression."""

from illogical.evaluable import Evaluable
from illogical.expression.comparison.comparison import Comparison


class Prefix(Comparison):
    """Has prefix comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable, symbol="PREFIX") -> None:
        super().__init__(
            "<prefixes>",
            symbol,
            lambda left, right: isinstance(left, str)
            and isinstance(right, str)
            and right.startswith(left),
            left,
            right,
        )

    def __repr__(self) -> str:
        return f"Prefix({repr(self.operands[0])}, {repr(self.operands[1])})"
