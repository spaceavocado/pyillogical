"""Is present comparison expression."""

from illogical.evaluable import Evaluable, Kind
from illogical.expression.comparison.comparison import Comparison

KIND = Kind('Present')

class Present(Comparison):
    """Is None comparison expression."""

    def __init__(self, operator: Evaluable) -> None:
        super().__init__(
            "<is present>",
            KIND,
            lambda operator: operator is not None,
            operator
        )
