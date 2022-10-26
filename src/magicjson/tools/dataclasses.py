"""
Dataclass register in order to deserialize dataclasses.
"""
from ..exceptions import MagicJSONError

dataclass_register: dict[str, type] = {}


def magicjson_dataclass(cls):
    if cls.__name__ in dataclass_register:
        raise MagicJSONError(f"Dataclass with name {cls.__name__} already in dataclass registry")
    dataclass_register[cls.__name__] = cls
    return cls
