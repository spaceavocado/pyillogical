"""Less or equal comparison expression."""

from illogical.evaluable import Evaluable
from illogical.expression.comparison.comparison import Comparison


class Le(Comparison):
    """Less or equal comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable, symbol="<=") -> None:
        super().__init__("<=", symbol, lambda left, right: left <= right, left, right)

    def __repr__(self) -> str:
        return f"Le({repr(self.operands[0])}, {repr(self.operands[1])})"
