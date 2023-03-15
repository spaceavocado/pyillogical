"""Is present comparison expression."""

from illogical.evaluable import Evaluable
from illogical.expression.comparison.comparison import Comparison


class Present(Comparison):
    """Is None comparison expression."""

    def __init__(self, operator: Evaluable, symbol="PRESENT") -> None:
        super().__init__(
            "<is present>", symbol, lambda operator: operator is not None, operator
        )

    def __repr__(self) -> str:
        return f"Present({repr(self.operands[0])})"
