from magicjson import serializer, deserializer


def register_path_serializer():
    from pathlib import Path

    @serializer(cls=Path)
    def serialize_path(pth: Path):
        return str(pth)

    @deserializer(cls=Path)
    def deserialize_path(data: str):
        return Path(data)
