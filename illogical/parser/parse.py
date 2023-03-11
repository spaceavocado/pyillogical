# pylint: disable=locally-disabled, too-few-public-methods

"""Expression parser."""

from typing import Iterable
from illogical.evaluable import Evaluable, Evaluated, Expression, Kind, is_primitive
from illogical.expression.comparison.comparison import Comparison
from illogical.expression.logical.logical import Logical
from illogical.operand.collection import Collection
from illogical.operand.reference import IgnoredPaths, IgnoredPathsRx, Reference, SerializeFrom, \
    SerializeTo, default_serialize_from, default_serialize_to
from illogical.expression.logical.and_exp import And
from illogical.expression.logical.or_exp import Or
from illogical.expression.logical.nor import Nor
from illogical.expression.logical.xor import Xor
from illogical.expression.logical.not_exp import Not
from illogical.expression.comparison.eq import Eq
from illogical.expression.comparison.ne import Ne
from illogical.expression.comparison.gt import Gt
from illogical.expression.comparison.ge import Ge
from illogical.expression.comparison.lt import Lt
from illogical.expression.comparison.le import Le
from illogical.expression.comparison.in_exp import In
from illogical.expression.comparison.nin import Nin
from illogical.expression.comparison.overlap import Overlap
from illogical.expression.comparison.prefix import Prefix
from illogical.expression.comparison.suffix import Suffix
from illogical.expression.comparison.none import Non
from illogical.expression.comparison.present import Present
from illogical.operand.value import Value

class UnexpectedExpressionInput(Exception):
    """Unexpected expression input."""

class UnexpectedExpression(Exception):
    """Unexpected expression."""

class UnexpectedOperand(Exception):
    """Invalid undefined operand"."""

# Expression identifiers
AND = Kind("AND")
OR = Kind("OR")
NOR = Kind("NOR")
XOR = Kind("XOR")
NOT = Kind("NOT")
EQ = Kind("EQ")
NE = Kind("NE")
GT = Kind("GT")
GE = Kind("GE")
LT = Kind("LT")
LE = Kind("LE")
IN = Kind("IN")
NIN = Kind("NIN")
OVERLAP = Kind("OVERLAPS")
PREFIX = Kind("PREFIX")
SUFFIX = Kind("SUFFIX")
NONE = Kind("NONE")
PRESENT = Kind("PRESENT")

DEFAULT_OPERATOR_MAPPING = {
    # Logical
    AND:     "AND",
    OR:      "OR",
    NOR:     "NOR",
    XOR:     "XOR",
    NOT:     "NOT",
    # Comparison
    EQ:      "==",
    NE:      "!=",
    GT:      ">",
    GE:      ">=",
    LT:      "<",
    LE:      "<=",
    NONE:     "NONE",
    PRESENT: "PRESENT",
    IN:      "IN",
    NIN:     "NOT IN",
    OVERLAP: "OVERLAP",
    PREFIX:  "PREFIX",
    SUFFIX:  "SUFFIX",
}

DEFAULT_ESCAPE_CHARACTER = "\\"

OperatorMapping = dict[Kind, str]
"""
Mapping of the operators. The key is unique operator symbol, and the value is the key used to
represent the given operator in the raw expression.

Example:

from illogical.parser.parse import Options, DEFAULT_OPERATOR_MAPPING, AND

    Copy default mapping:

operator_mapping = DEFAULT_OPERATOR_MAPPING.copy()

    Override the mapping for AND expression to use "&&" as operator. E.g.:
    ["&&", 1, 1] vs default ["AND", 1, 1]

operator_mapping[AND] = "&&"

illogical = Illogical(Options(operator_mapping=operator_mapping))

Default mapping:

DEFAULT_OPERATOR_MAPPING = {
    # Logical
    AND:     "AND",
    OR:      "OR",
    NOR:     "NOR",
    XOR:     "XOR",
    NOT:     "NOT",
    # Comparison
    EQ:      "==",
    NE:      "!=",
    GT:      ">",
    GE:      ">=",
    LT:      "<",
    LE:      "<=",
    NONE:     "NONE",
    PRESENT: "PRESENT",
    IN:      "IN",
    NIN:     "NOT IN",
    OVERLAP: "OVERLAP",
    PREFIX:  "PREFIX",
    SUFFIX:  "SUFFIX",
}
"""

def unary_handler(symbol: str, handler) -> Comparison | Logical:
    """Factory for a new instance of unary expression."""

    return lambda operands: handler(operands[0], symbol)

def binary_handler(symbol: str, handler) -> Comparison | Logical:
    """Factory for a new instance of binary expression."""

    return lambda operands: handler(operands[0], operands[1], symbol)

def logical_handler(not_symbol: str, nor_symbol: str):
    """
    Factory for a new instance of many expression with dependency on other symbols.
    """

    def handler(symbol: str, handler) -> Comparison | Logical:
        return lambda operands: handler(
            operands,
            symbol,
            not_symbol=not_symbol,
            nor_symbol=nor_symbol
        )

    return handler

def get_operator_handlers(operator_mapping: OperatorMapping) -> dict[Kind, Comparison | Logical]:
    """Create operator handler map"""

    unary_expressions = {
        operator_mapping[symbol]:
            unary_handler(operator_mapping[symbol], handler) for symbol, handler in (
                (NONE, Non),
                (PRESENT, Present),
                (NOT, Not),
            )
    }

    binary_expressions = {
        operator_mapping[symbol]:
            binary_handler(operator_mapping[symbol], handler) for symbol, handler in (
                (EQ, Eq),
                (NE, Ne),
                (GT, Gt),
                (GE, Ge),
                (LT, Lt),
                (LE, Le),
                (IN, In),
                (NIN, Nin),
                (OVERLAP, Overlap),
                (PREFIX, Prefix),
                (SUFFIX, Suffix)
            )
    }

    many_handler = logical_handler(operator_mapping[NOT], operator_mapping[NOR])

    many_expressions = {
        operator_mapping[symbol]:
            many_handler(operator_mapping[symbol], handler) for symbol, handler in (
                (AND, And),
                (OR, Or),
                (NOR, Nor),
                (XOR, Xor),
            )
    }

    return {**unary_expressions, **binary_expressions, **many_expressions}

class Options:
    """Parsing options."""

    def __init__(
        self,
        operator_mapping: OperatorMapping = None,
        reference_from: SerializeFrom = default_serialize_from,
        reference_to: SerializeTo = default_serialize_to,
        escape_character: str = DEFAULT_ESCAPE_CHARACTER,
        ignored_paths: IgnoredPaths = None,
        ignored_path_rx: IgnoredPathsRx = None,
    ) -> None:
        self.reference_from = reference_from
        self.reference_to = reference_to
        self.escape_character = escape_character
        self.ignored_paths = ignored_paths
        self.ignored_path_rx = ignored_path_rx

        mapping = operator_mapping if operator_mapping else DEFAULT_OPERATOR_MAPPING

        self.escaped_operators = (operator for operator in mapping.values())
        self.operator_handlers: dict[Kind, Comparison | Logical] = \
            get_operator_handlers(mapping)

def is_escaped(val: str, escape_character: str) -> bool:
    """Is the value escaped predicate."""

    return len(escape_character) > 0 and val.startswith(escape_character)

def to_reference_address(reference, reference_from: SerializeFrom) -> str | None:
    """Get reference address from raw reference input."""

    if isinstance(reference, str):
        return reference_from(reference)

    return None

def create_operand(val, options: Options) -> Reference | Value | Collection:
    """Create operand from the raw input."""

    if isinstance(val, (list, set, tuple)):
        if len(val) == 0:
            raise UnexpectedOperand()

        return Collection(
            [parse(operand, options) for operand in val],
            options.escape_character, options.escaped_operators
        )

    address = to_reference_address(val, options.reference_from)
    if address:
        return Reference(
            address,
            options.reference_to,
            options.ignored_paths,
            options.ignored_path_rx
        )

    if not is_primitive(val):
        raise UnexpectedOperand()

    return Value(val)

def create_expression(
    expression: Iterable[Evaluated],
    options: Options
) -> Comparison | Logical:
    """Create an logical or comparison expression from the raw input."""

    operator = expression[0]
    operands = expression[1:]

    handler = options.operator_handlers.get(operator)
    if handler is None:
        raise UnexpectedExpression()

    return handler([parse(operand, options) for operand in operands])

def parse(expression: Expression, options: Options = Options()) -> Evaluable:
    """Parse raw expression into evaluable."""

    if expression is None:
        raise UnexpectedExpressionInput()

    if not isinstance(expression, (list, set, tuple)):
        return create_operand(expression, options)

    if len(expression) < 2:
        return create_operand(expression, options)

    if isinstance(expression[0], str) and is_escaped(expression[0], options.escape_character):
        return create_operand([expression[0][1:], *expression[1:]], options)

    try:
        return create_expression(expression, options)
    except UnexpectedExpression:
        return create_operand(expression, options)
