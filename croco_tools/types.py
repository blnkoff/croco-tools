from dataclasses import dataclass
from typing import TypedDict


@dataclass
class Table:
    name: str
    columns: list[str]


class LoggingConfig(TypedDict):
    enable: bool
    level: str


class Proxy(TypedDict):
    host: str
    port: int
    username: str
    password: str
