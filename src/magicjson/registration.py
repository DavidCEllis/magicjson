"""
Registers for class serialization/deserialization
"""
from typing import Any, Optional, Callable, Union, NamedTuple

from .exceptions import RegistrationError

# Types natively serializable by the stdlib json moddule
native_serializable = Union[None, bool, int, float, str, list, dict]

# Register of classes and functions to call when serializing
serialize_register: list["SerializerInfo"] = []

# Map from aliases to methods to deserialize
deserialize_register: dict[str, Callable[[native_serializable], Any]] = {}


class SerializerInfo(NamedTuple):
    identifier: Callable[[object], bool]
    serializer_method: Callable[[object], native_serializable]
    deserializer_name: Optional[str]


def serializer(
        *,
        cls: Optional[type] = None,
        identifier: Optional[Callable[[object], bool]] = None,
        deserializer_name: Optional[str] = None,
        deserialize_auto: bool = True,
):
    """

    :param cls: class to use for isinstance serializer checks
    :param identifier: identifier to use for identifier(obj) checks
    :param deserializer_name: name to lookup for deserializer function
    :param deserialize_auto: automatically use cls.__name__ for
                             deserializing classes
    :return:
    """
    if cls and identifier:
        raise TypeError("serializer requires an identifier XOR a class, not both")
    elif not (cls or identifier):
        raise TypeError("serializer requires either a cls or an identifier")

    # the cls method is just convenience for isinstance identifiers
    if cls:
        identifier = lambda obj: isinstance(obj, cls)
        if deserialize_auto and not deserializer_name:
            deserializer_name = cls.__name__

    def wrapper(func: callable):
        serialize_register.append(SerializerInfo(identifier, func, deserializer_name))
        return func
    return wrapper


def deserializer(
        *,
        cls: type = None,
        name: str = None
):
    """
    :param cls: Class to be serialized
    :param name: Name to use to look up deserialization method (default is the class name if provided)
    """
    name = name if name else cls.__name__
    if name in deserialize_register:
        raise RegistrationError(f"Class with alias or name {name} has already been registered.")

    def wrapper(func):
        deserialize_register[name] = func
        return func
    return wrapper
