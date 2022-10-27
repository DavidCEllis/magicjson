"""Test more complicated round trips"""
from dataclasses import dataclass
from contextlib import contextmanager

from magicjson import dumps, loads
from magicjson.tools.stdlib_serializers import register_dataclass_serializer
from magicjson.tools.dataclasses import magicjson_dataclass, dataclass_register
from magicjson.registration import clear_registers
from magicjson.exceptions import MagicJSONError

from smalltest.tools import raises


@contextmanager
def register_cleanup():
    clear_registers()
    dataclass_register.clear()
    try:
        yield
    finally:
        dataclass_register.clear()
        clear_registers()


@register_cleanup()
def test_basic_dataclass_roundtrip():
    register_dataclass_serializer()

    @magicjson_dataclass
    @dataclass
    class X:
        x: str = "Test"

    x = X()

    assert loads(dumps(x)) == x


@register_cleanup()
def test_layered_dataclass_roundtrip():
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


@register_cleanup()
def test_matching_name_error():
    register_dataclass_serializer()

    @magicjson_dataclass
    @dataclass
    class Apple:
        x: int

    with raises(MagicJSONError) as e_info:
        @magicjson_dataclass
        @dataclass
        class Apple:
            pie: bool

    assert e_info.value.args[0] == "Dataclass with name Apple already in dataclass registry"


@register_cleanup()
def test_deserialize_failure():
    register_dataclass_serializer()

    @magicjson_dataclass
    @dataclass
    class X:
        data: str = "test"

    test_x = X()
    json_x = dumps(test_x)

    # Simulate loading in a separate instance by clearing the dataclass register
    dataclass_register.clear()

    with raises(MagicJSONError) as e_info:
        reload = loads(json_x)

    assert e_info.value.args[0] == "Could not find dataclass matching X to deserialize."
    assert e_info.value.args[1] == "@magicjson_dataclass decorator must be applied to class definition."


@register_cleanup()
def test_deserialize_non_strict():
    register_dataclass_serializer(strict=False)

    @magicjson_dataclass
    @dataclass
    class X:
        data: str = "test"

    test_x = X()
    json_x = dumps(test_x)

    # Simulate loading in a separate instance by clearing the dataclass register
    dataclass_register.clear()

    # in non-strict mode, dataclasses would reserialize to plain dicts
    reload = loads(json_x)
    assert reload == {"data": "test"}
