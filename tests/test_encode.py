import json

from magicjson import __version__, JSONRegister

from pytest import raises


def test_object_dumps():
    version = __version__

    register = JSONRegister()

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

    @register.cls_encoder(cls=Serializable)
    def serialize_cls(inst):
        return {'x': inst.x}

    @register.cls_encoder(cls=Serializable2, auto_name=False)
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
    assert register.dumps(serialize_data) == json.dumps(expected_data)


def test_failure():

    register = JSONRegister()

    class Unserializable:
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            return f"Serializable(x={self.x})"

    with raises(TypeError) as e_info:
        register.dumps([Unserializable(1)])
