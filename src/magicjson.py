from typing import Any, Optional
from collections.abc import Callable

__version__ = "v0.0.2a"


class RegisterError(Exception):
    pass


class SerializerInfo:
    def __init__(
            self,
            identifier: Callable[[object], bool],
            method: Callable[[object], Any],
            name: Optional[str] = None,
    ):
        self.identifier = identifier
        self.method = method
        self.name = name

    def __repr__(self):
        return f"SerializerInfo(identifier={self.identifier}, method={self.method}, name={self.name})"

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return (self.identifier, self.method, self.name) == (other.identifier, other.method, other.name)
        return NotImplemented

    def __iter__(self):
        yield from [self.identifier, self.method, self.name]


class JSONRegister:
    def __init__(self):
        self.serialize_register = []
        self.deserialize_register = {}

    # Registration Methods
    def register_serializer(
            self,
            identifier: Callable[[object], bool],
            method: Callable[[object], Any],
            name: Optional[str] = None,
    ):
        """
        Register a serialization method

        :param identifier: function that returns True on objects that
                           method should be used to serialize
        :param method: function to use to serialize identified objects
        :param name: Name for a deserializer to recreate the original object
        """
        self.serialize_register.append(
            SerializerInfo(identifier, method, name)
        )

    def register_cls_serializer(
            self,
            cls: type,
            method: Callable[[object], Any],
            name: Optional[str] = None,
            auto_name: bool = True
    ):
        """
        Register a serialization method for a class

        :param cls: Class this serialization method is for
        :param method: function to convert instances to serializable
                       objects.
        :param name: Name for a deserializer to recreate the instance
        :param auto_name: Automatically use the class name as the name
        """
        identifier = lambda obj: isinstance(obj, cls)
        if name is None and auto_name:
            name = cls.__name__
        self.serialize_register.append(
            SerializerInfo(identifier, method, name)
        )

    def serializer(
            self,
            identifier: Callable[[object], bool],
            name: Optional[str] = None,
    ):
        def wrapper(method: Callable[[object], Any]):
            self.register_serializer(identifier, method, name)
            return method
        return wrapper

    def cls_serializer(
            self,
            cls: type,
            name: Optional[str] = None,
            auto_name: bool = True,
    ):
        def wrapper(method: Callable[[object], Any]):
            self.register_cls_serializer(cls, method, name, auto_name)
            return method
        return wrapper

    def register_deserializer(self, name, method):
        if name in self.deserialize_register:
            raise RegisterError(f"Name {name} is already used in the register.")

        self.deserialize_register[name] = method

    def register_cls_deserializer(self, cls, method):
        self.register_deserializer(cls.__name__, method)

    def deserializer(self, name):
        def wrapper(method):
            self.register_deserializer(name, method)
            return method
        return wrapper

    def cls_deserializer(self, cls):
        def wrapper(method):
            self.register_cls_deserializer(cls, method)
            return method
        return wrapper

    def default(self, o):
        """
        default method to provide to json.dumps or equivalent

        use: json.dumps(obj, default=json_register.default)
        """
        for identifier, method, name in reversed(self.serialize_register):
            if identifier(o):
                if name:
                    result = {
                        "_magicjson": __version__,
                        "_deserializer": name,
                        "contents": method(o),
                    }
                else:
                    result = method(o)
                return result

        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

    def deserialize(self, data):
        if isinstance(data, dict):
            if '_magicjson' in data:
                # First deserialize anything further down the chain
                converted_data = self.deserialize(data["contents"])
                # Then use the stored method to convert back to python
                deserializer_name = data["_deserializer"]
                if deserializer_name not in self.deserialize_register:
                    raise RegisterError(
                        f"{data['_deserializer']} is not registered as a deserializer"
                    )
                method = self.deserialize_register[deserializer_name]
                data = method(converted_data)
            else:
                for key in data.keys():
                    data[key] = self.deserialize(data[key])
        elif isinstance(data, list):
            # Iterate over indices as we are replacing values
            for i in range(len(data)):
                data[i] = self.deserialize(data[i])
        return data
