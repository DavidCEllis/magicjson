from contextlib import contextmanager

from magicjson.registration import (
    serializer, deserializer, serialize_register,
    deserialize_register, SerializerInfo, RegistrationError
)
from smalltest.tools import raises


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
def test_add_serializer():
    from pathlib import Path

    method = lambda obj: isinstance(obj, Path)

    @serializer(identifier=method)
    def serialize_path(pth):
        return str(pth)

    assert serialize_register == [SerializerInfo(method, serialize_path, None)]


@register_cleanup()
def test_add_serializer_cls():
    from pathlib import Path

    @serializer(cls=Path)
    def serialize_path(pth):
        return str(pth)

    assert serialize_register[0].serializer_method == serialize_path
    assert serialize_register[0].deserializer_name == 'Path'


@register_cleanup()
def test_add_serializer_errors():
    with raises(TypeError) as e_info:
        @serializer(identifier=lambda obj: True, cls=object)
        def fake_serialize(obj):
            pass

    with raises(TypeError) as e_info:
        @serializer()
        def fake_serialize(obj):
            pass


@register_cleanup()
def test_add_deserializer():
    from pathlib import Path

    @deserializer(name='Path')
    def deserialize_path(data):
        return Path(data)

    assert deserialize_register['Path'] == deserialize_path


@register_cleanup()
def test_double_deserializer_error():
    from pathlib import Path

    @deserializer(cls=Path)
    def deserialize_path(data):
        return Path(data)

    with raises(RegistrationError) as e_info:
        @deserializer(cls=Path)
        def deserialize_path_again(data):
            return Path(data)
