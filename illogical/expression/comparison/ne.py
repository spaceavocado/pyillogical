"""Not equal comparison expression."""

from illogical.evaluable import Evaluable, Kind
from illogical.expression.comparison.comparison import Comparison

KIND = Kind('Ne')

class Ne(Comparison):
    """Not equal comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable) -> None:
        super().__init__(
            "!=",
            KIND,
            lambda left, right: left is not right,
            left,
            right
        )
