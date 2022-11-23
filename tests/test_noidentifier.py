import json

from magicjson import JSONRegister


from pytest import raises


def test_no_identifier():
    """
    Bug/Bugfix
    Only serialize the correct object
    """
    class Test1:
        def __init__(self, x, y):
            self.x, self.y = x, y

    class Test2:
        def __init__(self, x, y):
            self.x, self.y = x, y

    register = JSONRegister()

    @register.cls_encoder(cls=Test2, auto_name=False)
    def serialize_test2(obj):
        return {'x': obj.x, 'y': obj.y}

    testobj = Test1(42, 'apples')

    with raises(TypeError) as e_info:
        _ = json.dumps(testobj, default=register.default)

    error = "Object of type Test1 is not JSON serializable"

    assert e_info.value.args[0] == error
