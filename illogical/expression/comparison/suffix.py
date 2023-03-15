"""Has suffix comparison expression."""

from illogical.evaluable import Evaluable
from illogical.expression.comparison.comparison import Comparison


class Suffix(Comparison):
    """Has suffix comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable, symbol="SUFFIX") -> None:
        super().__init__(
            "<with suffix>",
            symbol,
            lambda left, right: isinstance(left, str)
            and isinstance(right, str)
            and left.endswith(right),
            left,
            right,
        )

    def __repr__(self) -> str:
        return f"Suffix({repr(self.operands[0])}, {repr(self.operands[1])})"
