"""
Dataclass register in order to deserialize dataclasses.
"""
from magicjson import serializer, deserializer
from magicjson.exceptions import MagicJSONError

dataclass_register: dict[str, type] = {}


def magicjson_dataclass(cls):
    if cls.__name__ in dataclass_register:
        raise MagicJSONError(f"Dataclass with name {cls.__name__} already in dataclass registry")
    dataclass_register[cls.__name__] = cls
    return cls


def register_dataclass_serializer(strict=True):
    """

    :param strict: True: MagicJson error if a deserialization method does not exist
                   False: Return a dictionary if a deserialization method does not exist
    :return:
    """
    # Lazy import
    from dataclasses import is_dataclass, fields

    @serializer(identifier=is_dataclass, deserializer_name='dataclass')
    def serialize_dataclass(dc):
        data = {
            f.name: getattr(dc, f.name) for f in fields(dc)
        }
        data['__class__.__name__'] = dc.__class__.__name__

        return data

    @deserializer(name='dataclass')
    def deserialize_dataclass(data):
        class_name = data.pop('__class__.__name__')
        if class_name in dataclass_register:
            cls = dataclass_register[class_name]
        else:
            if strict:
                raise MagicJSONError(
                    f"Could not find dataclass matching {class_name} to deserialize.",
                    "@magicjson_dataclass decorator must be applied to class definition."
                )
            else:
                return data
        return cls(**data)