"""Plain value operand."""

from illogical.evaluable import Evaluable, Primitive


class Value(Evaluable):
    """Value operand."""

    def __init__(self, val: Primitive):
        self.val = val

    def evaluate(self, _):
        return self.val

    def simplify(self, _):
        return self.val

    def serialize(self):
        return self.val

    def __str__(self):
        return f'"{self.val}"' if isinstance(self.val, str) else str(self.val).lower()

    def __repr__(self) -> str:
        return (
            f'Value("{self.val}")'
            if isinstance(self.val, str)
            else f"Value({self.val})"
        )
