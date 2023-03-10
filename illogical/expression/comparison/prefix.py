"""Has prefix comparison expression."""

from illogical.evaluable import Evaluable, Kind
from illogical.expression.comparison.comparison import Comparison

KIND = Kind('Prefix')

class Prefix(Comparison):
    """Has prefix comparison expression."""

    def __init__(self, left: Evaluable, right: Evaluable) -> None:
        super().__init__(
            "<prefixes>",
            KIND,
            lambda left, right: isinstance(left, str) and isinstance(right, str) and \
                right.startswith(left),
            left,
            right
        )
