from pathlib import Path

from magicjson import __version__, JSONRegister, RegisterError
import json

from pytest import raises


def test_deserialize_basic():
    fake_path = "usr/bin/python"

    data = (f'{{'
            f'"obj1": {{'
            f'"_magicjson": "{__version__}", '
            f'"_deserializer": "Path", '
            f'"contents": "{fake_path}"'
            f'}} '
            f'}}')

    register = JSONRegister()

    register.register_cls_deserializer(Path, Path)

    assert register.deserialize(json.loads(data)) == {"obj1": Path(fake_path)}


def test_deserialize_fail():
    fake_path = "usr/bin/python"

    data = (f'{{'
            f'"obj1": {{'
            f'"_magicjson": "{__version__}", '
            f'"_deserializer": "Path", '
            f'"contents": "{fake_path}"'
            f'}} '
            f'}}')

    register = JSONRegister()

    with raises(RegisterError) as e_info:
        _ = register.deserialize(json.loads(data))


def test_deserialize_list():
    fake_path = 'usr/bin/python'
    fake_path2 = 'usr/bin/python2'

    data = (f'[{{'
            f'"_magicjson": "{__version__}", '
            f'"_deserializer": "Path", '
            f'"contents": "{fake_path}"'
            f'}}, {{'
            f'"_magicjson": "{__version__}", '
            f'"_deserializer": "Path", '
            f'"contents": "{fake_path2}"'
            f'}}'
            f']')

    register = JSONRegister()
    register.register_cls_deserializer(Path, Path)

    result = register.deserialize(json.loads(data))

    assert result == [Path(fake_path), Path(fake_path2)]
