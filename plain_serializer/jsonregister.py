class JSONRegister:
    def __init__(self):
        self.registry = []

    def register(self, cls, func):
        self.registry.append((cls, func))

    def register_function(self, cls):
        """Decorate a function"""
        def wrapper(func):
            self.register(cls, func)
            return func
        return wrapper

    @property
    def register_method(self):
        """Decorate a class method"""
        class RegisterDecorator:
            def __init__(inst, func):
                inst.func = func

            def __set_name__(inst, owner, name):
                self.register(owner, inst.func)
                setattr(owner, name, inst.func)

        return RegisterDecorator

    def default(self, o):
        for cls, func in self.registry:
            if isinstance(o, cls):
                return func(o)
        raise TypeError(
            f"Object of type {o.__class__.__name__} is not JSON serializable"
        )


if __name__ == "__main__":
    # Demo to show serialization of objects inside other objects
    from dataclasses import dataclass, fields
    from pathlib import Path

    json_register = JSONRegister()

    # Serialize classes that already exist with simple methods
    json_register.register(Path, str)

    # Decorate methods on a class you create
    @dataclass
    class FilePath:
        filename: str
        folder: Path

        @json_register.register_method
        def serialize(self):
            return {f.name: getattr(self, f.name) for f in fields(self)}

    @dataclass
    class Onion:
        # Extra layer to demonstrate recursion
        layer: FilePath

    # register functions you create on classes you didn't create
    @json_register.register_function(Onion)
    def serialize(self):
        return {f.name: getattr(self, f.name) for f in fields(self)}

    fp = {
        "Python3.10": Onion(FilePath("python310", Path("/usr/bin"))),
        "Python3.11": Onion(FilePath("python311", Path("/usr/bin"))),
    }

    import json
    s = json.dumps(fp, default=json_register.default)
    print(s)
