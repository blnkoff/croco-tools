from collections import UserDict
from dataclasses import dataclass
from typing import TypedDict, Optional, Self
from croco_tools.tools import *


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


class _SnakedDict(UserDict):
    def __init__(self, __dict: Optional[dict | Self] = None):
        user_cased_dict = __dict if __dict else {}

        snaked_dict = dict()
        key_map = dict()
        key_occuring = set()
        keys_to_remove = set()

        for user_key, value in user_cased_dict.items():
            if (snaked_key := snake_case(user_key)) in key_occuring:
                keys_to_remove.add(user_key)
            else:
                key_occuring.add(snaked_key)
                key_map[snaked_key] = user_key
                snaked_dict[snaked_key] = value

        for key in keys_to_remove:
            user_cased_dict.pop(key)

        self._user_cased_dict = user_cased_dict

        self._key_map = key_map
        super().__init__(snaked_dict)

    def __setitem__(self, key, value):
        snake_key = snake_case(key)

        user_key = self._key_map[snake_key]

        self._user_cased_dict[user_key] = value
        super().__setitem__(snake_key, value)

    @classmethod
    def recursive_snake(cls, __dict: Optional[dict] = None):
        user_dict = __dict if __dict else None
        for key, value in user_dict.items():
            if isinstance(value, dict):
                user_dict[key] = cls(value)
            elif isinstance(value, list):
                user_dict[key] = [cls(item) if isinstance(item, dict) else item for item in value]

        return cls(user_dict)

    def user_case(self) -> dict:
        return self._user_cased_dict

    def pascal_case(self) -> dict:
        pascal_cased_dict = {pascal_case(key): value for key, value in self.data.items()}
        return pascal_cased_dict

    def camel_case(self) -> dict:
        camel_cased_dict = {camel_case(key): value for key, value in self.data.items()}
        return camel_cased_dict

    def constant_case(self) -> dict:
        constant_cased_dict = {constant_case(key): value for key, value in self.data.items()}
        return constant_cased_dict

    def kebab_case(self) -> dict:
        kebab_cased_dict = {kebab_case(key): value for key, value in self.data.items()}
        return kebab_cased_dict


class SnakedDict(UserDict):
    def __init__(self, __dict: Optional[dict] = None):
        snaked_dict = _SnakedDict.recursive_snake(__dict)
        super().__init__(snaked_dict)
