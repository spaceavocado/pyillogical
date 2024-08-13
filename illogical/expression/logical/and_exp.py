# pylint: disable=locally-disabled, duplicate-code

"""And logical expression."""

from typing import Iterable

from illogical.evaluable import Context, Evaluable, Evaluated, flatten_context
from illogical.expression.logical.logical import (
    InvalidLogicalExpression, InvalidLogicalExpressionOperand, Logical)


class And(Logical):
    """And logical expression."""

    def __init__(self, operands: Iterable[Evaluable], symbol: str = "AND", **_) -> None:
        if len(operands) < 2:
            raise InvalidLogicalExpression()

        super().__init__("AND", symbol, *operands)

    def evaluate(self, context: Context) -> bool:
        context = flatten_context(context)

        for operand in self.operands:
            res = operand.evaluate(context)
            if not isinstance(res, bool):
                raise InvalidLogicalExpressionOperand()
            elif not res:
                return False

        return True

    def simplify(self, context: Context) -> Evaluated | Evaluable:
        context = flatten_context(context)
        simplified = []

        for operand in self.operands:
            res = operand.simplify(context)
            if isinstance(res, bool):
                if not res:
                    return False
                continue

            simplified.append(res if isinstance(res, Evaluable) else operand)

        if len(simplified) == 0:
            return True

        if len(simplified) == 1:
            return simplified[0]

        return And(simplified, self.symbol)

    def __repr__(self) -> str:
        args = [
            f'[{", ".join(repr(operand) for operand in self.operands)}]',
            f'symbol="{self.symbol}"',
        ]
        return f'And({", ".join(args)})'
