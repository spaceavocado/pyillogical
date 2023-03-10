"""Expression parser."""

from typing import Iterable
from illogical.evaluable import Evaluated, Expression, Kind, is_primitive
from illogical.expression.comparison.comparison import Comparison
from illogical.expression.logical.logical import Logical
from illogical.operand.collection import Collection
from illogical.operand.reference import IgnoredPaths, IgnoredPathsRx, Reference, SerializeFrom, \
    SerializeTo, default_serialize_from, default_serialize_to
from illogical.expression.logical.and_exp import KIND as AND, And
from illogical.expression.logical.or_exp import KIND as OR, Or
from illogical.expression.logical.nor import KIND as NOR, Nor
from illogical.expression.logical.xor import KIND as XOR, Xor
from illogical.expression.logical.not_exp import KIND as NOT, Not
from illogical.expression.comparison.eq import KIND as EQ, Eq
from illogical.expression.comparison.ne import KIND as NE, Ne
from illogical.expression.comparison.gt import KIND as GT, Gt
from illogical.expression.comparison.ge import KIND as GE, Ge
from illogical.expression.comparison.lt import KIND as LT, Lt
from illogical.expression.comparison.le import KIND as LE, Le
from illogical.expression.comparison.includes import KIND as IN, In
from illogical.expression.comparison.nin import KIND as NIN, Nin
from illogical.expression.comparison.overlap import KIND as OVERLAPS, Overlap
from illogical.expression.comparison.prefix import KIND as PREFIX, Prefix
from illogical.expression.comparison.suffix import KIND as SUFFIX, Suffix
from illogical.expression.comparison.none import KIND as NONE, Non
from illogical.expression.comparison.present import KIND as PRESENT, Present
from illogical.operand.value import Value
from illogical.options import Options

class UnexpectedExpressionInput(Exception):
    """Unexpected expression input."""

class UnexpectedExpression(Exception):
    """Unexpected expression."""

class UnexpectedOperand(Exception):
    """Invalid undefined operand"."""

OperatorMapping = dict[Kind, str]

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
    OVERLAPS: "OVERLAP",
    PREFIX:  "PREFIX",
    SUFFIX:  "SUFFIX",
}

def get_operator_handlers(operator_mapping: dict[Kind, str]) -> dict[Kind, Comparison | Logical]:
    """Create operator handler map"""

    return {
        # Logical
        operator_mapping[AND]:      And,
        operator_mapping[OR]:       Or,
        operator_mapping[NOR]:      Nor,
        operator_mapping[XOR]:      Xor,
        operator_mapping[NOT]:      Not,
        # Comparison
        operator_mapping[EQ]:       Eq,
        operator_mapping[NE]:       Ne,
        operator_mapping[GT]:       Gt,
        operator_mapping[GE]:       Ge,
        operator_mapping[LT]:       Lt,
        operator_mapping[LE]:       Le,
        operator_mapping[NONE]:     Non,
        operator_mapping[PRESENT]:  Present,
        operator_mapping[IN]:       In,
        operator_mapping[NIN]:      Nin,
        operator_mapping[OVERLAPS]: Overlap,
        operator_mapping[PREFIX]:   Prefix,
        operator_mapping[SUFFIX]:   Suffix,
    }

class ParseOptions(Options):
    """Parsing options."""

    def __init__(
        self,
        operator_mapping: OperatorMapping = None,
        reference_from: SerializeFrom = default_serialize_from,
        reference_to: SerializeTo = default_serialize_to,
        escape_character: str = "\\",
        ignored_paths: IgnoredPaths = None,
        ignored_path_rx: IgnoredPathsRx = None,
    ) -> None:
        super().__init__(
            operator_mapping,
            reference_from,
            reference_to,
            escape_character,
            ignored_paths,
            ignored_path_rx
        )

        self.escaped_operators = (operator for operator in operator_mapping.values())
        self.operator_handlers: dict[Kind, Comparison | Logical] = \
            get_operator_handlers(
                operator_mapping if operator_mapping else DEFAULT_OPERATOR_MAPPING
            )

def is_escaped(val: str, escape_character: str) -> bool:
    """Is the value escaped predicate."""

    return len(escape_character) > 0 and val.startswith(escape_character)

def to_reference_address(reference, reference_from: SerializeFrom) -> str | None:
    """Get reference address from raw reference input."""

    if isinstance(reference, str):
        return reference_from(reference)

    return None

def create_operand(val, options: ParseOptions) -> Reference | Value | Collection:
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
    options: ParseOptions
) -> Comparison | Logical:
    """Create an logical or comparison expression from the raw input."""

    operator = expression[0]
    operands = expression[1:]

    handler = options.operator_handlers.get(operator)
    if handler is None:
        raise UnexpectedExpression()

    return handler(*[parse(operand, options) for operand in operands])

def parse(expression: Expression, options: ParseOptions = ParseOptions()):
    """Parse raw expression into evaluable."""

    if expression is None:
        raise UnexpectedExpressionInput()

    if not isinstance(expression, (list, set, tuple)):
        return create_operand(expression, options)

    if len(expression) < 2:
        return create_operand(expression, options)

    if is_escaped(expression[0], options.escape_character):
        return create_operand([expression[0][1:], *expression[1:]], options)

    return create_expression(expression, options)
