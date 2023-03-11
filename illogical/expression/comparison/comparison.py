"""Comparison expression."""

from typing import Iterable, Callable
from illogical.evaluable import Context, Evaluated, Evaluable, is_evaluable

class Comparison(Evaluable):
    """Comparison expression."""

    def __init__(
        self,
        operator: str,
        symbol: str,
        comparison: Callable[[Iterable[Evaluated]], bool],
        *operands: Iterable[Evaluable]
    ) -> None:
        self.operator = operator
        self.symbol = symbol
        self.comparison = comparison
        self.operands = operands

    def evaluate(self, context: Context) -> bool:
        try:
            return self.comparison(*[operand.evaluate(context) for operand in self.operands])
        except TypeError:
            return False

    def simplify(self, context: Context):
        res = []
        for operand in self.operands:
            val = operand.simplify(context)
            if is_evaluable(val):
                return self

            res.append(val)

        return self.comparison(*res)

    def serialize(self):
        return [self.symbol, *[operand.serialize() for operand in self.operands]]

    def __str__(self):
        res = f"({str(self.operands[0])} {self.operator}"
        if len(self.operands) > 1:
            res += ' ' + ' '.join(str(operand) for operand in self.operands[1:])
        return res + ")"
