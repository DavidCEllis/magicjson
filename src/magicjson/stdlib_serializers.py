"""
Basic serializers for unserializable stdlib classes
"""
from decimal import Decimal
from pathlib import Path

from .registration import serializer, deserializer


@serializer(Path)
def serialize_path(pth: Path):
    return str(pth)


@deserializer(Path)
def deserialize_path(data: str):
    return Path(data)


@serializer(Decimal)
def serialize_decimal(no: Decimal):
    return str(no)


@deserializer(Decimal)
def deserialize_decimal(data: str):
    return Decimal(data)
