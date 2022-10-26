"""
Basic serializers for unserializable stdlib classes
"""
from ..registration import serializer, deserializer
from ..exceptions import MagicJsonError


def register_path_serializer():
    from pathlib import Path

    @serializer(cls=Path)
    def serialize_path(pth: Path):
        return str(pth)

    @deserializer(cls=Path)
    def deserialize_path(data: str):
        return Path(data)


def register_dataclass_serializer(strict=True):
    """

    :param strict: True: MagicJson error if a deserialization method does not exist
                   False: Return a dictionary if a deserialization method does not exist
    :return:
    """
    from dataclasses import is_dataclass, fields
    from .dataclasses import dataclass_register

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
                raise MagicJsonError(
                    f"Could not find dataclass matching {class_name} to deserialize.",
                    "@magicjson_dataclass decorator must be applied to class definition."
                )
            else:
                return data
        return cls(**data)
