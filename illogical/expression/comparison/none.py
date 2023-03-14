"""Is None comparison expression."""

from illogical.evaluable import Evaluable
from illogical.expression.comparison.comparison import Comparison


class Non(Comparison):
    """Is None comparison expression."""

    def __init__(self, operator: Evaluable, symbol = "NONE") -> None:
        super().__init__(
            "<in none>",
            symbol,
            lambda operator: operator is None,
            operator
        )
