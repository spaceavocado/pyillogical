"""Not logical unary expression."""

from illogical.evaluable import Context, Evaluable, Evaluated, flatten_context
from illogical.expression.logical.logical import (
    InvalidLogicalExpressionOperand, Logical)


class Not(Logical):
    """Not logical unary expression."""

    def __init__(self, operand: Evaluable, symbol: str = "NOT", **_) -> None:
        super().__init__("NOT", symbol, operand)

    def evaluate(self, context: Context) -> bool:
        context = flatten_context(context)
        res = self.operands[0].evaluate(context)

        if not isinstance(res, bool):
            raise InvalidLogicalExpressionOperand()

        return not res

    def simplify(self, context: Context) -> Evaluated | Evaluable:
        context = flatten_context(context)
        res = self.operands[0].simplify(context)

        if isinstance(res, bool):
            return not res

        return self

    def __repr__(self) -> str:
        args = [
            f"{repr(self.operands[0])}",
            f'symbol="{self.symbol}"',
        ]
        return f'Not({", ".join(args)})'
