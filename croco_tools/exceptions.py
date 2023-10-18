from typing import Any
from .types import Table


class InvalidColumns(Exception):
    """Raised when provided columns not containing in Table"""

    def __init__(self, columns: list[str], table: Table) -> None:
        super().__init__(f"Columns {columns} doesn't contain in table {table.name}. Supported columns - {table.columns}")


class NoLoggingLevel(Exception):
    """Raised when there is no logging level in config file"""

    def __init__(self) -> None:
        super().__init__(f"Logging level is not configured in config")


class InvalidLoggingLevel(TypeError):
    """Raised when logging level doesn't represent on of the values: info, debug, error, critical"""

    def __init__(self, value: Any) -> None:
        super().__init__(f"Logging level doesn't represent on of the values: info, debug, error, critical. Provided"
                         f"value is {value}")
