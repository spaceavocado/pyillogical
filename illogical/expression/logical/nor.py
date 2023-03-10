"""Negative or logical expression."""

from typing import Iterable
from illogical.evaluable import Context, Evaluable, Evaluated, Kind
from illogical.expression.logical.logical import InvalidLogicalExpression, Logical
from illogical.expression.logical.not_exp import Not

KIND = Kind('Nor')

class Nor(Logical):
    """Negative or logical expression."""

    def __init__(self, *operands: Iterable[Evaluable]) -> None:
        if len(operands) < 2:
            raise InvalidLogicalExpression()

        super().__init__(
            "NOR",
            KIND,
            *operands
        )

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
            return Not(simplified[0])

        return Nor(*simplified)
