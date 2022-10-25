import magicjson.stdlib_serializers
from magicjson.registration import serialize_register, deserialize_classes, deserialize_methods

from pathlib import Path
from decimal import Decimal


def test_serialize_register():
    assert serialize_register == [
        (Path, magicjson.stdlib_serializers.serialize_path),
        (Decimal, magicjson.stdlib_serializers.serialize_decimal)
    ]


def test_deserialize_classes():
    assert deserialize_classes == {Path: 'Path', Decimal: 'Decimal'}


def test_deserialize_methods():
    assert deserialize_methods == {
        'Path': magicjson.stdlib_serializers.deserialize_path,
        'Decimal': magicjson.stdlib_serializers.deserialize_decimal
    }
