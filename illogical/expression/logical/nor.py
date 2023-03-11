# pylint: disable=locally-disabled, duplicate-code

"""Negative or logical expression."""

from typing import Iterable
from illogical.evaluable import Context, Evaluable, Evaluated
from illogical.expression.logical.logical import InvalidLogicalExpression, Logical
from illogical.expression.logical.not_exp import Not

class Nor(Logical):
    """Negative or logical expression."""

    def __init__(
        self,
        operands: Iterable[Evaluable],
        symbol: str = "NOR",
        not_symbol: str = "NOT",
        **_
    ) -> None:
        if len(operands) < 2:
            raise InvalidLogicalExpression()

        super().__init__(
            "NOR",
            symbol,
            *operands
        )

        self.not_symbol = not_symbol

    def evaluate(self, context: Context) -> bool:
        for operand in self.operands:
            res = operand.evaluate(context)
            if isinstance(res, bool) and res:
                return False

        return True

    def simplify(self, context: Context) -> Evaluated | Evaluable:
        simplified = []

        for operand in self.operands:
            res = operand.simplify(context)
            if isinstance(res, bool):
                if res:
                    return False
                continue

            simplified.append(res)

        if len(simplified) == 0:
            return True

        if len(simplified) == 1:
            return Not(simplified[0], self.not_symbol)

        return Nor(simplified, self.symbol, self.not_symbol)
