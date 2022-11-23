"""
This is a basic single file serializer that only handles adding methods
to convert to JSON and does not deal with deserialization.

Example usage in the if __name__ == '__main__' block.

While the asdict function of dataclasses provides recursion through the
dataclass, this is not necessary as the json module is already going to
do that and will also handle going through any other containers.
"""
from typing import Callable, Optional


class JSONRegister:
    def __init__(self, dumps_func=None):
        self.serializer_registry = []

        if dumps_func is None:
            import json
            self.dumps_func = json.dumps
        else:
            self.dumps_func = dumps_func

    def serializer(
            self,
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
            self.serializer_registry.append((identifier, func))
            return func

        return wrapper

    def default(self, o):
        for identifier, method in self.serializer_registry:
            if identifier(o):
                return method(o)
        else:
            raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

    def dumps(self, data, **kwargs) -> str:
        if 'default' in kwargs:
            default = kwargs.pop('default')

            def metadefault(o):
                try:
                    return default(o)
                except TypeError:
                    return self.default(o)

            return self.dumps_func(data, default=metadefault, **kwargs)
        else:
            return self.dumps_func(data, default=self.default, **kwargs)


if __name__ == "__main__":
    """Demo to show serialization of objects inside other objects"""
    from dataclasses import dataclass, is_dataclass, fields
    from pathlib import Path

    json_register = JSONRegister()


    @json_register.serializer(identifier=is_dataclass)
    def serialize_dataclasses(dc):
        # Don't use asdict, no need to recurse here
        data = {
            f.name: getattr(dc, f.name)
            for f in fields(dc)
        }
        return data

    @json_register.serializer(cls=Path)
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

    print(json_register.dumps(fp))
