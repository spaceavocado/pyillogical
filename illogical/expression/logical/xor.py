"""Exclusive or logical expression."""

from typing import Iterable
from illogical.evaluable import Context, Evaluable, Evaluated, Kind
from illogical.expression.logical.logical import InvalidLogicalExpression, Logical
from illogical.expression.logical.nor import Nor
from illogical.expression.logical.not_exp import Not

KIND = Kind('Xor')

class Xor(Logical):
    """Exclusive or logical expression."""

    def __init__(self, *operands: Iterable[Evaluable]) -> None:
        if len(operands) < 2:
            raise InvalidLogicalExpression()

        super().__init__(
            "XOR",
            KIND,
            *operands
        )

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
                return Not(simplified[0])
            return simplified[0]

        if truthy == 1:
            return Nor(*simplified)

        return Xor(*simplified)
