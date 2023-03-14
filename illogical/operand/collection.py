"""Collection operand."""

from typing import Iterable

from illogical.evaluable import Context, Evaluable, is_evaluable

EscapeCharacter = str
r"""
Charter used to escape fist value within a collection, if the value contains operator value.

Example:
- `["==", 1, 1]` // interpreted as EQ expression
- `["\==", 1, 1]` // interpreted as a collection
"""


class InvalidCollection(Exception):
    """
    Collection operand must have at least 1 item.
    """

def should_be_escaped(subject, escaped_operators: set[str]) -> bool:
    """Should be the input escaped, i.e. operator character, predicate."""

    if subject is None:
        return False

    return isinstance(subject, str) and subject in escaped_operators


def escape_operator(operator: str, escape_character: str) -> str:
    """Escape operator symbol"""

    return f"{escape_character}{operator}"

class Collection(Evaluable):
    """Collection operand."""

    def __init__(
        self,
        items: Iterable[Evaluable],
        escape_character: EscapeCharacter = "\\",
        escaped_operators: set[str] = ()
    ):
        if len(items) == 0:
            raise InvalidCollection()

        self.items = items
        self.escape_character = escape_character
        self.escaped_operators = escaped_operators

    def evaluate(self, context: Context):
        return [item.evaluate(context) for item in self.items]

    def simplify(self, context: Context):
        res = []
        for item in self.items:
            val = item.simplify(context)
            if is_evaluable(val):
                return self

            res.append(val)

        return res

    def serialize(self):
        head = self.items[0].serialize()
        if should_be_escaped(head, self.escaped_operators):
            head = escape_operator(head, self.escape_character)

        return [head, *[item.serialize() for item in self.items[1:]]]

    def __str__(self):
        return f"[{', '.join(str(item) for item in self.items)}]"
