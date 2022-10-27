"""
This is a basic single file serializer that only handles adding methods
to convert to JSON and does not deal with deserialization.

Example usage in the if __name__ == '__main__' block.

While the asdict function of dataclasses provides recursion through the
dataclass, this is not necessary as the json module is already going to
do that and will also handle going through any other containers.
"""
from typing import Callable, Optional

serializer_registry = []


def serializer(
        *,
        identifier: Optional[Callable[[object], bool]] = None,
        cls: Optional[type] = None,
):
    """
    Given an identifier OR a class object (type), register a
    serialization method for the objects

    :param identifier: Method to identify serializable objects
    :param cls: Class to serialize
    :return:
    """
    if cls and identifier:
        raise TypeError("serializer requires an identifier XOR a class, not both")
    elif not (cls or identifier):
        raise TypeError("serializer requires either a cls or an identifier")

    # the cls method is just convenience for isinstance identifiers
    if cls:
        identifier = lambda obj: isinstance(obj, cls)

    def wrapper(func: Callable):
        serializer_registry.append((identifier, func))
        return func
    return wrapper


def default(o):
    for identifier, method in serializer_registry:
        if identifier(o):
            return method(o)
    else:
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


def dumps(data, dumps_func: Optional[Callable] = None, **kwargs) -> str:
    if not dumps_func:
        import json
        dumps_func = json.dumps
    return dumps_func(data, default=default, **kwargs)


if __name__ == "__main__":
    """Demo to show serialization of objects inside other objects"""
    from dataclasses import dataclass, is_dataclass, fields
    from pathlib import Path

    @serializer(identifier=is_dataclass)
    def serialize_dataclasses(dc):
        # Don't use asdict, no need to recurse here
        data = {
            f.name: getattr(dc, f.name)
            for f in fields(dc)
        }
        return data

    @serializer(cls=Path)
    def serialize_path(pth):
        return str(pth)


    @dataclass
    class FilePath:
        filename: str
        folder: Path

    @dataclass
    class Onion:
        """Extra layer to demonstrate recursion"""
        layer: FilePath

    fp = {
        "Python3.10": Onion(FilePath('python', Path('/usr/bin'))),
        "Python3.11": Onion(FilePath('python', Path('/usr/bin'))),
    }

    print(dumps(fp))
