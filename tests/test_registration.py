from magicjson.registration import (
    serializer, deserializer, serialize_register,
    deserialize_register, SerializerInfo, RegistrationError
)
from smalltest.tools import raises


def test_add_serializer():
    from pathlib import Path
    # Start with a clear list
    serialize_register.clear()

    method = lambda obj: isinstance(obj, Path)

    @serializer(identifier=method)
    def serialize_path(pth):
        return str(pth)

    assert serialize_register == [SerializerInfo(method, serialize_path, None)]

    serialize_register.clear()


def test_add_serializer_cls():
    serialize_register.clear()

    from pathlib import Path

    @serializer(cls=Path)
    def serialize_path(pth):
        return str(pth)

    assert serialize_register[0].serializer_method == serialize_path
    assert serialize_register[0].deserializer_name == 'Path'

    serialize_register.clear()


def test_add_serializer_errors():
    serialize_register.clear()

    with raises(TypeError) as e_info:
        @serializer(identifier=lambda obj: True, cls=object)
        def fake_serialize(obj):
            pass

    with raises(TypeError) as e_info:
        @serializer()
        def fake_serialize(obj):
            pass

    serialize_register.clear()


def test_add_deserializer():
    from pathlib import Path
    # Start with a clear dict
    deserialize_register.clear()

    @deserializer(name='Path')
    def deserialize_path(data):
        return Path(data)

    assert deserialize_register['Path'] == deserialize_path

    deserialize_register.clear()


def test_double_deserializer_error():
    from pathlib import Path
    deserialize_register.clear()

    @deserializer(cls=Path)
    def deserialize_path(data):
        return Path(data)

    with raises(RegistrationError) as e_info:
        @deserializer(cls=Path)
        def deserialize_path_again(data):
            return Path(data)
