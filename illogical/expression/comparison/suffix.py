"""Has suffix comparison expression."""

from illogical.evaluable import Evaluable, Kind
from illogical.expression.comparison.comparison import Comparison

KIND = Kind('Suffix')

class Suffix(Comparison):
    """Has suffix comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable) -> None:
        super().__init__(
            "<with suffix>",
            KIND,
            lambda left, right: isinstance(left, str) and isinstance(right, str) and \
                left.endswith(right),
            left,
            right
        )
