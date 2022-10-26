"""
Registers for class serialization/deserialization
"""
import typing

from .exceptions import RegistrationError

# Types natively serializable by the stdlib json moddule
native_serializable = typing.Union[None, bool, int, float, str, list, dict]

# Register of classes and functions to call when serializing
serialize_register: list[tuple[type, typing.Callable]] = []

# Map from classess to the names of the aliases for lookups
deserialize_classes: dict[type, str] = {}

# Map from aliases to methods to deserialize
deserialize_methods: dict[str, typing.Callable] = {}


def serializer(*, cls: type, identifier: typing.Callable[[object], bool]):
    """

    :param cls: class to use for isinstance serializer checks
    :param identifier: identifier to use for identifier(obj) checks
    :return:
    """
    def wrapper(func: callable):
        serialize_register.append((cls, func))
        return func
    return wrapper


def deserializer(*, cls: type, alias: str = None):
    """
    :param cls: Class to be serialized
    :param alias: Name to use to look up deserialization method (default is the class name)
    """
    name = alias if alias else cls.__name__
    if name in deserialize_methods:
        raise RegistrationError(f"Class with alias or name {name} has already been registered.")

    deserialize_classes[cls] = name

    def wrapper(func):
        deserialize_methods[name] = func
        return func
    return wrapper
