from collections import UserDict
from dataclasses import dataclass
from typing import TypedDict, Optional
from croco_tools.tools import snake_case


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


class SnakeDict(UserDict):
    def __init__(self, __dict: Optional[dict] = None):
        snake_cased_dict = {snake_case(key): value for key, value in __dict.items()}
        self._user_cased_dict = user_cased_dict = __dict if __dict else {}

        key_map = {}
        for snake_key, pascal_key in zip(snake_cased_dict, user_cased_dict):
            key_map[snake_key] = pascal_key

        self._key_map = key_map
        super().__init__(snake_cased_dict)

    def __setitem__(self, key, value):
        snake_key = snake_case(key)
        pascal_key = self._key_map[snake_key]

        self._user_cased_dict[pascal_key] = value
        super().__setitem__(snake_key, value)

    def user_case(self) -> dict:
        return self._user_cased_dict
