"""Greater or equal comparison expression."""

from illogical.evaluable import Evaluable, Kind
from illogical.expression.comparison.comparison import Comparison

KIND = Kind('Ge')

class Ge(Comparison):
    """Greater or equal comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable) -> None:
        super().__init__(
            ">=",
            KIND,
            lambda left, right: left >= right,
            left,
            right
        )
