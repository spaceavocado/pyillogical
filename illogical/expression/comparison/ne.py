"""Not equal comparison expression."""

from illogical.evaluable import Evaluable
from illogical.expression.comparison.comparison import Comparison


class Ne(Comparison):
    """Not equal comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable, symbol="!=") -> None:
        super().__init__(
            "!=", symbol, lambda left, right: left is not right, left, right
        )

    def __repr__(self) -> str:
        return f"Ne({repr(self.operands[0])}, {repr(self.operands[1])})"
