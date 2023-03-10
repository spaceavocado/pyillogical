"""Reference operand."""

import re
from enum import Enum
from typing import Callable, Iterable, Tuple
from illogical.evaluable import Context, Kind, Primitive, Evaluable

KIND = Kind('reference')

_DATA_TYPE_RX = r'^.+\.\(([A-Z][a-z]+)\)$'
_DATA_TYPE_TRIM_RX = r'.\(([A-Z][a-z]+)\)$'
_FLOAT_RX = r'^\d+\.\d+$'
_FLOAT_TRIM_RX = r'\.\d+$'
_INT_RX = r'^0$|^[1-9]\d*$'
_NESTED_REFERENCE_RX = r'{([^{}]+)}'

SerializeFrom = Callable[[str], str]
"""
A function used to determine if the operand is a reference type,
otherwise evaluated as a static value.
"""

SerializeTo = Callable[[str], str]
"""
A function used to transform the operand into the reference annotation stripped form. I.e. remove
any annotation used to detect the reference type. E.g. "$Reference" => "Reference".
"""

IgnoredPaths = Iterable[str]
"""
Reference paths which should be ignored while simplification is applied. Must be an exact match.
"""

IgnoredPathsRx = Iterable[str]
"""
Reference paths which should be ignored while simplification is applied.
Matching regular expression patterns.
"""

class DataType(Enum):
    """Referenced value data type."""

    UNDEFINED = 0
    NUMBER = 1
    INTEGER = 2
    FLOAT = 3
    STRING = 4
    BOOLEAN = 5

def get_data_type(address: str) -> DataType:
    """Get reference data type from the address, if present."""

    match = re.search(_DATA_TYPE_RX, address)
    if not match:
        return DataType.UNDEFINED

    data_type = match.group(1)

    if data_type == "Number":
        return DataType.NUMBER

    if data_type == "Integer":
        return DataType.INTEGER

    if data_type == "Float":
        return DataType.FLOAT

    if data_type == "String":
        return DataType.STRING

    if data_type == "Boolean":
        return DataType.BOOLEAN

    return DataType.UNDEFINED

def trim_data_type(address: str) -> str:
    """Trim data type annotation from the reference address."""

    return re.sub(_DATA_TYPE_TRIM_RX, "", address)

def is_ignored_path(
    path: str,
    ignored_paths: IgnoredPaths = None,
    ignored_path_rx: IgnoredPathsRx = None
) -> bool:
    """
    Is ignored path by simplification options (ignored paths, ignored paths rx) predicate.
    """

    if ignored_paths:
        if any(needle == path for needle in ignored_paths):
            return True

    if ignored_path_rx:
        if any(re.search(pattern, path) is not None for pattern in ignored_path_rx):
            return True

    return False

def to_number(val):
    """
    Convert val to number if possible. Boolean is converted to 1, 0.
    """

    if isinstance(val, bool):
        return 1 if val is True else 0

    if isinstance(val, (int, float)):
        return val

    if isinstance(val, str):
        if re.search(_FLOAT_RX, val) is not None:
            return float(val)
        if re.search(_INT_RX, val) is not None:
            return int(val)

    return val

def to_int(val):
    """
    Convert val to int if possible.
    Boolean is converted to 1, 0.
    Float string is floored.
    """

    if isinstance(val, bool):
        return 1 if val is True else 0

    if isinstance(val, (int, float)):
        return int(val)

    if isinstance(val, str):
        if re.search(_FLOAT_RX, val) is not None:
            return int(re.sub(_FLOAT_TRIM_RX, "", val))
        if re.search(_INT_RX, val) is not None:
            return int(val)

    return val

def to_float(val):
    """
    Convert val to float if possible.
    """

    if isinstance(val, (int, float)):
        return float(val)

    if isinstance(val, str):
        if re.search(_INT_RX, val) is not None:
            return float(val)
        if re.search(_FLOAT_RX, val) is not None:
            return float(val)

    return val

def to_string(val):
    """
    Convert val to string.
    """

    if isinstance(val, bool):
        return str(val).lower()

    return str(val)

def to_boolean(val):
    """
    Convert val to boolean if possible. Number is converted True, False if 1, 0 respectively.
    """

    if isinstance(val, bool):
        return val

    if isinstance(val, (int, float)):
        return True if val == 1 else False

    if isinstance(val, str):
        if val.lower() in ("true", "1"):
            return True
        if val.lower() in ("false", "0"):
            return False

def context_lookup(context: Context, path: str) -> Tuple[str, Primitive | None]:
    """Try to get a value from the context object based on the reference path."""

    match = re.search(_NESTED_REFERENCE_RX, path)
    while match:
        start, end = match.span()
        _, val = context_lookup(context, match.groups(0)[0])
        if val is None:
            return (path, None)

        path = path[0:start] + str(val) + path[end:]
        match = re.search(_NESTED_REFERENCE_RX, path)


    return (path, context.get(path))


def evaluate(context: Context, path: str, data_type: DataType) -> Tuple[str, Primitive]:
    """
    Evaluate the reference at given path from the context.
    Resolved value is typed, if data type is provided.
    """

    resolved_path, value = context_lookup(context, path)

    if value is None:
        return (resolved_path, None)

    if data_type == DataType.NUMBER:
        return (resolved_path, to_number(value))

    if data_type == DataType.INTEGER:
        return (resolved_path, to_int(value))

    if data_type == DataType.FLOAT:
        return (resolved_path, to_float(value))

    if data_type == DataType.BOOLEAN:
        return (resolved_path, to_boolean(value))

    if data_type == DataType.STRING:
        return (resolved_path, to_string(value))

    return (resolved_path, value)


def default_serialize_from(address: str) -> str:
    """Default deserialization."""

    return address[1:] if len(address) > 1 and address.startswith("$") else ""

def default_serialize_to(operand: str) -> str:
    """Default serialization."""

    return f"${operand}"

class Reference(Evaluable):
    """Reference operand."""

    kind: KIND

    def __init__(
        self,
        address: str,
        serialize_to: SerializeTo = default_serialize_to,
        simplify_ignored_paths: IgnoredPaths = None,
        simplify_ignored_path_rx: IgnoredPathsRx = None,
    ) -> None:
        self.address = address
        self.serialize_to = serialize_to
        self.ignored_paths = simplify_ignored_paths
        self.ignored_path_rx = simplify_ignored_path_rx
        self.data_type = get_data_type(address)
        self.path = trim_data_type(address)


    def evaluate(self, context: Context):
        _, res = evaluate(context, self.path, self.data_type)
        return res

    def simplify(self, context: Context):
        path, res = evaluate(context, self.path, self.data_type)

        if res is not None or is_ignored_path(path, self.ignored_paths, self.ignored_path_rx):
            return res

        return self


    def serialize(self):
        path = self.path

        if self.data_type is not DataType.UNDEFINED:
            path = f"{path}.({self.data_type.name.capitalize()})"

        return self.serialize_to(path)

    def __str__(self):
        return f"{{{self.address}}}"
