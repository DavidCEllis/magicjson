import json
from contextlib import contextmanager

from magicjson import __version__, dumps
from magicjson.registration import serializer, clear_registers

try:
    from smalltest.tools import raises
except ImportError:
    from pytest import raises


@contextmanager
def register_cleanup():
    clear_registers()
    try:
        yield
    finally:
        clear_registers()


@register_cleanup()
def test_object_dumps():
    version = __version__

    class Serializable:
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            return f"Serializable(x={self.x})"

    class Serializable2:
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            return f"Serializable2(x={self.x})"

    @serializer(cls=Serializable)
    def serialize_cls(inst):
        return {'x': inst.x}

    @serializer(cls=Serializable2, deserialize_auto=False)
    def serialize_cls2(inst):
        return {'x': inst.x}

    serialize_data = {
        "First": Serializable(1),
        "Second": Serializable2(2)
    }
    expected_data = {
        "First": {
            "_magicjson": version,
            "_deserializer": "Serializable",
            "contents": {"x": 1}
        },
        "Second": {"x": 2}
    }
    assert dumps(serialize_data) == json.dumps(expected_data)


@register_cleanup()
def test_failure():

    class Unserializable:
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            return f"Serializable(x={self.x})"

    with raises(TypeError) as e_info:
        dumps([Unserializable(1)])
