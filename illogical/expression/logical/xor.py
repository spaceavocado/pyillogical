"""Exclusive or logical expression."""

from typing import Iterable
from illogical.evaluable import Context, Evaluable, Evaluated
from illogical.expression.logical.logical import InvalidLogicalExpression, Logical
from illogical.expression.logical.nor import Nor
from illogical.expression.logical.not_exp import Not

class Xor(Logical):
    """Exclusive or logical expression."""

    def __init__(
        self,
        operands: Iterable[Evaluable],
        symbol: str = "XOR",
        not_symbol: str = "NOT",
        nor_symbol: str = "NOR",
        **kwargs
    ) -> None:
        if len(operands) < 2:
            raise InvalidLogicalExpression()

        super().__init__(
            "XOR",
            symbol,
            *operands
        )

        self.not_symbol = not_symbol
        self.nor_symbol = nor_symbol

    def evaluate(self, context: Context) -> bool:
        out = None

        for operand in self.operands:
            res = operand.evaluate(context)
            if isinstance(res, bool) and res:
                out = res if out is None else out ^ res

        return out if out else False

    def simplify(self, context: Context) -> Evaluated | Evaluable:
        truthy = 0
        simplified = []

        for operand in self.operands:
            res = operand.simplify(context)
            if isinstance(res, bool):
                if res:
                    truthy += 1
                if truthy > 1:
                    return False
                continue

            simplified.append(res)

        if len(simplified) == 0:
            return truthy == 1

        if len(simplified) == 1:
            if truthy == 1:
                return Not(simplified[0], self.not_symbol)
            return simplified[0]

        if truthy == 1:
            return Nor(simplified, self.nor_symbol, self.not_symbol)

        return Xor(simplified, self.symbol, self.not_symbol, self.nor_symbol)
