"""
Basic serializers for unserializable stdlib classes
"""
from .registration import serializer, deserializer
from .exceptions import MagicJsonError


def register_path_serializer():
    from pathlib import Path

    @serializer(cls=Path)
    def serialize_path(pth: Path):
        return str(pth)

    @deserializer(cls=Path)
    def deserialize_path(data: str):
        return Path(data)


def register_dataclass_serializer():
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
        import inspect
        class_name = data.pop('__class__.__name__')
        # Inspect up the stack for a dataclass matching this name
        for level in inspect.stack():
            if class_name in level.frame.f_locals:
                tmp_cls = level.frame.f_locals[class_name]
                if is_dataclass(tmp_cls):
                    cls = tmp_cls
                    break
        else:
            raise MagicJsonError(f"Could not find dataclass matching {class_name} to deserialize to.")

        return cls(**data)
