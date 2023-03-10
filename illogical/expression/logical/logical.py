"""Logical expression."""

from typing import Iterable
from illogical.evaluable import Kind, Evaluable

class InvalidLogicalExpression(Exception):
    """Non unary logical expression must have at least 2 operands"""

class Logical(Evaluable):
    """Logical expression."""

    def __init__(
        self,
        operator: str,
        kind: Kind,
        *operands: Iterable[Evaluable]
    ) -> None:
        self.operator = operator
        self.kind = kind
        self.operands = operands

    def serialize(self):
        return [self.kind, *[operand.serialize() for operand in self.operands]]

    def __str__(self):
        if len(self.operands) == 1:
            return f"({self.operator} {self.operands[0]})"
        return "(" + f" {self.operator} ".join(str(operand) for operand in self.operands) + ")"
