"""
Methods for converting python objects to JSON
"""
from typing import Union

from . import __version__
from .registration import serialize_register

# Types natively serializable by the stdlib json moddule
native_serializable = Union[None, bool, int, float, str, list, dict]


# default method to provide to json.dumps (or equivalent) to serialize objects
def default(o) -> native_serializable:
    for identifier, method, deserializer_name in serialize_register:
        if identifier(o):
            if deserializer_name:
                result = {
                    "_magicjson": __version__,
                    "_deserializer": deserializer_name,
                    "contents": method(o)
                }
                return result
            else:
                # Convert directly to the base type if no deserializer is given
                return method(o)
    else:
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


def dumps(data, method=None, **kwargs):
    if not method:
        import json
        method = json.dumps
    return method(data, default=default, **kwargs)
