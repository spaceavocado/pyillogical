# pylint: disable=locally-disabled, duplicate-code

"""Or logical expression."""

from typing import Iterable

from illogical.evaluable import Context, Evaluable, Evaluated
from illogical.expression.logical.logical import (InvalidLogicalExpression,
                                                  Logical)


class Or(Logical):
    """Or logical expression."""

    def __init__(
        self,
        operands: Iterable[Evaluable],
        symbol: str = "OR",
        **_
    ) -> None:
        if len(operands) < 2:
            raise InvalidLogicalExpression()

        super().__init__(
            "OR",
            symbol,
            *operands
        )

    def evaluate(self, context: Context) -> bool:
        for operand in self.operands:
            res = operand.evaluate(context)
            if isinstance(res, bool) and res:
                return True

        return False

    def simplify(self, context: Context) -> Evaluated | Evaluable:
        simplified = []

        for operand in self.operands:
            res = operand.simplify(context)
            if isinstance(res, bool):
                if res:
                    return True
                continue

            simplified.append(res)

        if len(simplified) == 0:
            return False

        if len(simplified) == 1:
            return simplified[0]

        return Or(simplified, self.symbol)
