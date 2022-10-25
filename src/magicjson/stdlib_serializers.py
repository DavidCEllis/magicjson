"""
Basic serializers for unserializable stdlib classes
"""
from decimal import Decimal
from pathlib import Path

from .registration import serializer, deserializer


@serializer(cls=Path)
def serialize_path(pth: Path):
    return str(pth)


@deserializer(cls=Path)
def deserialize_path(data: str):
    return Path(data)


@serializer(cls=Decimal)
def serialize_decimal(no: Decimal):
    return str(no)


@deserializer(cls=Decimal)
def deserialize_decimal(data: str):
    return Decimal(data)
