"""
This is a basic single file serializer that only handles adding methods
to convert to JSON and does not deal with deserialization.

Example usage in the if __name__ == '__main__' block.
"""


class JSONRegister:
    def __init__(self, *, dumps_func=None):
        self.serializer_registry = []

        if dumps_func is None:
            import json

            self.dumps_func = json.dumps
        else:
            self.dumps_func = dumps_func

    def register_serializer(self, cls, func):
        self.serializer_registry.append((cls, func))

    def serializer(self, cls: type):
        # Decorator form of register_serializer
        def wrapper(func):
            self.register_serializer(cls, func)
            return func

        return wrapper

    def default(self, o):
        for cls, method in self.serializer_registry:
            if isinstance(o, cls):
                return method(o)
        else:
            raise TypeError(
                f"Object of type {o.__class__.__name__} is not JSON serializable"
            )

    def dumps(self, obj, **kwargs) -> str:
        if "default" in kwargs:
            default = kwargs.pop("default")

            def metadefault(o):
                try:
                    return default(o)
                except TypeError:
                    return self.default(o)

            return self.dumps_func(obj, default=metadefault, **kwargs)
        else:
            return self.dumps_func(obj, default=self.default, **kwargs)


if __name__ == "__main__":
    # Demo to show serialization of objects inside other objects
    from dataclasses import dataclass, fields
    from pathlib import Path

    json_register = JSONRegister()

    def serialize_dataclass(dc):
        # Don't use asdict, no need to recurse here
        data = {f.name: getattr(dc, f.name) for f in fields(dc)}
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
        # Extra layer to demonstrate recursion
        layer: FilePath

    json_register.register_serializer(FilePath, serialize_dataclass)
    json_register.register_serializer(Onion, serialize_dataclass)

    fp = {
        "Python3.10": Onion(FilePath("python310", Path("/usr/bin"))),
        "Python3.11": Onion(FilePath("python311", Path("/usr/bin"))),
    }

    print(json_register.dumps(fp))
