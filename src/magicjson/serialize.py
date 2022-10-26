"""
Methods for converting python objects to JSON
"""

from . import __version__
from .registration import serialize_register


# default method to provide to json.dumps (or equivalent) to serialize objects
def default(o):
    for identifier, method, deserializer_name in serialize_register:
        if deserializer_name:
            if identifier(o):
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
