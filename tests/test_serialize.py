import json
from contextlib import contextmanager

from smalltest.tools import raises

from magicjson import __version__, dumps
from magicjson.registration import serializer, serialize_register, deserialize_register


@contextmanager
def register_cleanup():
    serialize_register.clear()
    deserialize_register.clear()
    try:
        yield
    finally:
        deserialize_register.clear()
        serialize_register.clear()


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
