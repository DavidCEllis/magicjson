from json import dumps, loads

from magicjson import JSONRegister

from pytest import raises



def test_recursive():
    """Test conversions that go through multiple serializers"""
    # Here the Test1 object defines its serializable form as Test2

    register = JSONRegister()

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

    @register.cls_encoder(cls=Test1)
    def serialize_test1(obj):
        return Test2(obj.x, obj.y)

    @register.cls_decoder(cls=Test1)
    def deserialize_test1(obj):
        return Test1(obj.x, obj.y)

    @register.cls_encoder(cls=Test2)
    def serialize_test2(obj):
        return {"x": obj.x, "y": obj.y}

    @register.cls_decoder(cls=Test2)
    def deserialize_test2(data):
        return Test2(**data)

    example = Test1(42, 'Apples')

    assert example == register.reconstruct(loads(dumps(example, default=register.default)))


def test_failed_recursive():
    """Test conversions try to go through multiple serializers"""

    register = JSONRegister()

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

    @register.cls_encoder(cls=Test1)
    def serialize_test1(obj):
        return Test2(obj.x, obj.y)

    example = Test1(42, 'Apples')

    with raises(TypeError) as e_info:
        dumps(example, default=register.default)

    assert e_info.value.args[0] == "Object of type Test2 is not JSON serializable"
