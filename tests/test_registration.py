from magicjson import JSONRegister, RegisterError
from magicjson import SerializerInfo

from pytest import raises


def test_add_serializer():
    from pathlib import Path

    register = JSONRegister()

    method = lambda obj: isinstance(obj, Path)

    @register.serializer(identifier=method)
    def serialize_path(pth):
        return str(pth)

    assert register.serialize_register == [SerializerInfo(method, serialize_path, None)]


def test_add_serializer_cls():
    from pathlib import Path

    register = JSONRegister()

    @register.cls_serializer(cls=Path)
    def serialize_path(pth):
        return str(pth)

    assert register.serialize_register[0].method == serialize_path
    assert register.serialize_register[0].name == 'Path'


def test_add_deserializer():
    from pathlib import Path

    register = JSONRegister()

    @register.deserializer(name='Path')
    def deserialize_path(data):
        return Path(data)

    assert register.deserialize_register['Path'] == deserialize_path


def test_double_deserializer_error():
    from pathlib import Path

    register = JSONRegister()

    @register.cls_deserializer(cls=Path)
    def deserialize_path(data):
        return Path(data)

    with raises(RegisterError) as e_info:
        @register.cls_deserializer(cls=Path)
        def deserialize_path_again(data):
            return Path(data)
