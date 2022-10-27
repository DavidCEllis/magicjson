"""Test serialization/deserialization of Path objects"""
from pathlib import Path
from contextlib import contextmanager

from magicjson import dumps, loads
from magicjson.registration import clear_registers
from magicjson.stdlib_serializers import register_path_serializer


@contextmanager
def register_cleanup():
    clear_registers()
    try:
        yield
    finally:
        clear_registers()


@register_cleanup()
def test_path_serializer():
    register_path_serializer()
    pth = Path('usr/bin/python')
    assert loads(dumps(pth)) == pth
