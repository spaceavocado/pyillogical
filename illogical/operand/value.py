"""Plain value operand."""

from illogical.evaluable import Kind, Primitive, Evaluable

KIND = Kind('value')

class Value(Evaluable):
    """Value operand."""

    kind = KIND

    def __init__(self, val: Primitive):
        self.val = val

    def evaluate(self, _):
        return self.val

    def simplify(self, _):
        return self.val

    def serialize(self):
        return self.val

    def __str__(self):
        return f'"{self.val}"' if isinstance(self.val, str) else str(self.val)
