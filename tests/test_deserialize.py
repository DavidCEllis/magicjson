from magicjson import loads, deserializer, __version__
from magicjson.registration import deserialize_register
from magicjson.exceptions import MissingDeserializerError

from smalltest.tools import raises

from pathlib import Path


def test_deserialize_basic():
    deserialize_register.clear()

    fake_path = "usr/bin/python"

    data = (f'{{'
            f'"obj1": {{'
            f'"_magicjson": "{__version__}", '
            f'"_deserializer": "Path", '
            f'"contents": "{fake_path}"'
            f'}} '
            f'}}')

    @deserializer(cls=Path)
    def deserialize_path(pth_str):
        return Path(pth_str)

    assert loads(data) == {"obj1": Path(fake_path)}

    deserialize_register.clear()


def test_deserialize_fail():
    deserialize_register.clear()

    fake_path = "usr/bin/python"

    data = (f'{{'
            f'"obj1": {{'
            f'"_magicjson": "{__version__}", '
            f'"_deserializer": "Path", '
            f'"contents": "{fake_path}"'
            f'}} '
            f'}}')

    with raises(MissingDeserializerError) as e_info:
        _ = loads(data)


def test_deserialize_list():
    deserialize_register.clear()
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

    @deserializer(cls=Path)
    def deserialize_path(pth):
        return Path(pth)

    result = loads(data)

    assert result == [Path(fake_path), Path(fake_path2)]
