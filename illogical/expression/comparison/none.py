"""Is None comparison expression."""

from illogical.evaluable import Evaluable, Kind
from illogical.expression.comparison.comparison import Comparison

KIND = Kind('None')

class Non(Comparison):
    """Is None comparison expression."""

    def __init__(self, operator: Evaluable) -> None:
        super().__init__(
            "<in none>",
            KIND,
            lambda operator: operator is None,
            operator
        )
