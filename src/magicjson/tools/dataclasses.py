"""
Dataclass register in order to deserialize dataclasses.
"""
dataclass_register: dict[str, type] = {}


def magicjson_dataclass(cls):
    dataclass_register[cls.__name__] = cls
    return cls
