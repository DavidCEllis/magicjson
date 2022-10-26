import magicjson.stdlib_serializers
from magicjson.registration import serialize_register, deserialize_register, SerializerInfo

from pathlib import Path
from decimal import Decimal


def test_serialize_register():
    assert len(serialize_register) == 2


def test_deserialize_methods():
    assert deserialize_register == {
        'Path': magicjson.stdlib_serializers.deserialize_path,
        'Decimal': magicjson.stdlib_serializers.deserialize_decimal
    }
