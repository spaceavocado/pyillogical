from illogical.operand.reference import IgnoredPaths, IgnoredPathsRx, SerializeFrom, SerializeTo, default_serialize_from, default_serialize_to
from illogical.parser.parse import OperatorMapping


class Options:
    """Illogical engine options."""

    def __init__(
        self,
        operator_mapping: OperatorMapping = None,
        reference_from: SerializeFrom = default_serialize_from,
        reference_to: SerializeTo = default_serialize_to,
        escape_character: str = "\\",
        ignored_paths: IgnoredPaths = None,
        ignored_path_rx: IgnoredPathsRx = None,
    ) -> None:
        self.operator_mapping = operator_mapping
        self.reference_from = reference_from
        self.reference_to = reference_to
        self.escape_character = escape_character
        self.ignored_paths = ignored_paths
        self.ignored_path_rx = ignored_path_rx
