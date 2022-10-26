"""Test more complicated round trips"""
from dataclasses import dataclass

from magicjson import dumps, loads
from magicjson.tools.stdlib_serializers import register_dataclass_serializer
from magicjson.tools.dataclasses import magicjson_dataclass, dataclass_register
from magicjson.registration import clear_registers


def test_basic_dataclass_roundtrip():
    # Start from empty registers
    clear_registers()
    dataclass_register.clear()

    register_dataclass_serializer()

    @magicjson_dataclass
    @dataclass
    class X:
        x: str = "Test"

    x = X()

    assert loads(dumps(x)) == x

    dataclass_register.clear()
    clear_registers()


def test_layered_dataclass_roundtrip():
    # Start from empty registers
    clear_registers()
    dataclass_register.clear()

    register_dataclass_serializer()

    @magicjson_dataclass
    @dataclass
    class X:
        x: list
        y: list
        z: list[int]

    @magicjson_dataclass
    @dataclass
    class Y:
        a: dict[str, "Z"]
        b: int

    @magicjson_dataclass
    @dataclass
    class Z:
        z: int

    z = Z(12)
    z2 = Z(2)
    z3 = Z(3)
    y = Y({'this_is_z': z, 'this_is_z2': z2}, 42)
    y2 = Y({'this_is_z3': z3}, 21)
    x = X(
        [y, y2],
        [z, z2, z3],
        [1, 2, 3, 4]
    )
    x2 = X(
        [z, y, y2],
        [z3, x],
        [4, 3, 2, 1]
    )
    datalist = [x, x2]
    datadict = {'x': x, 'x2': x2}

    assert loads(dumps(x)) == x
    assert loads(dumps(x2)) == x2
    assert loads(dumps(datalist)) == datalist
    assert loads(dumps(datadict)) == datadict
