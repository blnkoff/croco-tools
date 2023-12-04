from collections import UserDict
from dataclasses import dataclass
from typing import TypedDict, Optional, Self, Callable, Union
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


class _MultiCaseDict(UserDict):
    def __init__(self, __dict: dict | Self, case_handler: Callable[[str], str]):
        user_cased_dict = __dict if __dict else {}

        cased_dict = dict()
        key_map = dict()
        key_occuring = set()

        for user_key, value in user_cased_dict.items():
            if not (cased_key := case_handler(user_key)) in key_occuring:
                key_occuring.add(cased_key)
                key_map[cased_key] = user_key
                cased_dict[cased_key] = value

        self._case_handler = case_handler
        super().__init__(cased_dict)

    def __setitem__(self, key, value):
        case_handler = self._case_handler
        cased_key = case_handler(key)
        super().__setitem__(cased_key, value)

    @staticmethod
    def recursive_case(
            __dict: dict | Self,
            case_handler: Callable[[str], str]
    ) -> Self:
        user_dict = __dict
        new_dict = {}
        for key, value in user_dict.items():
            if isinstance(value, Union[dict, _MultiCaseDict]):
                new_dict[key] = _MultiCaseDict(value, case_handler)
            elif isinstance(value, list):
                new_dict[key] = [_MultiCaseDict(item, case_handler) if isinstance(item, Union[dict, _MultiCaseDict]) else item for item in value]
            else:
                new_dict[key] = value

        return _MultiCaseDict(new_dict, case_handler)

    def pascal_case(self) -> dict:
        pascal_cased_dict = {}
        pascal_cased_dict.update(_MultiCaseDict.recursive_case(self.data, pascal_case))
        return pascal_cased_dict

    def camel_case(self) -> dict:
        camel_cased_dict = {}
        camel_cased_dict.update(_MultiCaseDict.recursive_case(self.data, camel_case))
        return camel_cased_dict

    def constant_case(self) -> dict:
        constant_cased_dict = {}
        constant_cased_dict.update(_MultiCaseDict.recursive_case(self.data, constant_case))
        return constant_cased_dict

    def kebab_case(self) -> dict:
        kebab_cased_dict = {}
        kebab_cased_dict.update(_MultiCaseDict.recursive_case(self.data, kebab_case))
        return kebab_cased_dict

    def snake_case(self) -> dict:
        snake_cased_dict = {}
        snake_cased_dict.update(_MultiCaseDict.recursive_case(self.data, snake_case))
        return snake_cased_dict


class SnakedDict(_MultiCaseDict):
    def __init__(self, __dict: Optional[dict] = None):
        snaked_dict = _MultiCaseDict.recursive_case(__dict, snake_case)
        super().__init__(snaked_dict, snake_case)


class CameledDict(_MultiCaseDict):
    def __init__(self, __dict: Optional[dict] = None):
        cameled_dict = _MultiCaseDict.recursive_case(__dict, camel_case)
        super().__init__(cameled_dict, camel_case)
