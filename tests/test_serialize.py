from magicjson import __version__, dumps
import magicjson.stdlib_serializers


def test_decimaldump():
    from decimal import Decimal
    expected = f'{{"_magicjson": "{__version__}", "_deserializer": "Decimal", "contents": "3.14"}}'
    assert dumps(Decimal('3.14')) == expected
