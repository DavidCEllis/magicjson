from pathlib import Path
from contextlib import contextmanager

from magicjson import loads, deserializer, __version__
from magicjson.registration import deserialize_register
from magicjson.exceptions import MissingDeserializerError

from smalltest.tools import raises


@contextmanager
def register_cleanup():
    deserialize_register.clear()
    try:
        yield
    finally:
        deserialize_register.clear()


@register_cleanup()
def test_deserialize_basic():
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


@register_cleanup()
def test_deserialize_fail():
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


@register_cleanup()
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

    @deserializer(cls=Path)
    def deserialize_path(pth):
        return Path(pth)

    result = loads(data)

    assert result == [Path(fake_path), Path(fake_path2)]
