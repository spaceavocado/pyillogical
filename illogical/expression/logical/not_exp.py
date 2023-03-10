"""Not logical unary expression."""

from illogical.evaluable import Context, Evaluable, Evaluated
from illogical.expression.logical.logical import Logical

class InvalidNotExpression(Exception):
    """Logical NOT expression's operand must be evaluated to boolean value."""

class Not(Logical):
    """Not logical unary expression."""

    def __init__(self, operand: Evaluable, symbol: str = "NOT", **kwargs) -> None:
        super().__init__(
            "NOT",
            symbol,
            operand
        )

    def evaluate(self, context: Context) -> bool:
        res = self.operands[0].evaluate(context)

        if not isinstance(res, bool):
            raise InvalidNotExpression()

        return not res

    def simplify(self, context: Context) -> Evaluated | Evaluable:
        res = self.operands[0].simplify(context)
        if isinstance(res, bool):
            return not res

        return self
