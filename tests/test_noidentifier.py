from magicjson import serializer, dumps
from smalltest.tools import raises


def test_direct_conversion():
    class Test1:
        def __init__(self, x, y):
            self.x, self.y = x, y

    class Test2:
        def __init__(self, x, y):
            self.x, self.y = x, y

    @serializer(cls=Test2, deserialize_auto=False)
    def serialize_test2(obj):
        return {'x': obj.x, 'y': obj.y}

    testobj = Test1(42, 'apples')

    with raises(TypeError) as e_info:
        _ = dumps(testobj)

    error = "Object of type Test1 is not JSON serializable"

    assert e_info.value.args[0] == error
