"""Greater comparison expression."""

from illogical.evaluable import Evaluable
from illogical.expression.comparison.comparison import Comparison

class Gt(Comparison):
    """Greater comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable, symbol = ">") -> None:
        super().__init__(
            ">",
            symbol,
            lambda left, right: left > right,
            left,
            right
        )
