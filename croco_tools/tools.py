import re
from typing import Any, Literal, Type, TypedDict, get_args

__all__ = [
    'in_literal',
    'is_typed_dict',
    'snake_case',
    'camel_case',
    'pascal_case',
    'kebab_case',
    'constant_case'
]


def in_literal(value: Any, expected_type: Literal) -> bool:
    values = get_args(expected_type)
    return value in values


def is_typed_dict(value: Any, typed_dict: Type[TypedDict]) -> bool:
    typed_dict_keys = typed_dict.__annotations__.keys()

    try:
        value_keys = value.keys()
    except AttributeError:
        return False

    return typed_dict_keys == value_keys


def snake_case(s: str) -> str:
    """
    Convert a string to snake_case.
    """
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s)
    s = re.sub(r'\W+', '_', s).lower()
    s = re.sub(r'_+', '_', s)
    return s


def camel_case(s: str) -> str:
    """
    Convert a string to camelCase.
    """
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
    s = s[0].lower() + s[1:]
    return s


def pascal_case(s: str) -> str:
    """
    Convert a string to PascalCase.
    """
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return s


def constant_case(s: str) -> str:
    """
    Convert a string to CONSTANT_CASE.
    """
    s = re.sub(r'\W+', '_', s)
    return s.upper()


def kebab_case(s: str) -> str:
    """
    Convert a string to kebab-case
    """
    s = re.sub(r"(\s|_|-)+", " ", s)
    s = re.sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
               lambda mo: ' ' + mo.group(0).lower(), s)
    s = '-'.join(s.split())
    return s
