from contextlib import contextmanager

from magicjson import serializer, deserializer, dumps, loads
from magicjson.registration import clear_registers

from pytest import raises


@contextmanager
def register_cleanup():
    clear_registers()
    try:
        yield
    finally:
        clear_registers()


@register_cleanup()
def test_recursive():
    """Test conversions that go through multiple serializers"""
    # Here the Test1 object defines its serializable form as Test2

    class Test1:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __eq__(self, other):
            return isinstance(other, self.__class__) and ((self.x, self.y) == (other.x, other.y))

    class Test2:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    @serializer(cls=Test1)
    def serialize_test1(obj):
        return Test2(obj.x, obj.y)

    @deserializer(cls=Test1)
    def deserialize_test1(obj):
        return Test1(obj.x, obj.y)

    @serializer(cls=Test2)
    def serialize_test2(obj):
        return {"x": obj.x, "y": obj.y}

    @deserializer(cls=Test2)
    def deserialize_test2(data):
        return Test2(**data)

    example = Test1(42, 'Apples')

    assert example == loads(dumps(example))


register_cleanup()
def test_failed_recursive():
    """Test conversions try to go through multiple serializers"""

    # Here the Test1 object defines its serializable form as Test2
    # Test2 has no serializer so this should fail and mention this
    class Test1:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Test2:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    @serializer(cls=Test1)
    def serialize_test1(obj):
        return Test2(obj.x, obj.y)

    example = Test1(42, 'Apples')

    with raises(TypeError) as e_info:
        dumps(example)

    assert e_info.value.args[0] == "Object of type Test2 is not JSON serializable"
