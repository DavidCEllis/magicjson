"""
Methods for converting python objects to JSON
"""

from . import __version__
from registration import serialize_register, deserialize_classes


# default method to provide to json.dumps (or equivalent) to serialize objects
def default(o):
    for cls, method in serialize_register:
        if isinstance(o, cls):
            result = {
                "_magicjson": __version__,
                "_class": cls.__name__,
                "_alias": deserialize_classes[cls],
                "contents": method(o)
            }
            return result
    else:
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


def dumps(data, method=None, **kwargs):
    if not method:
        import json
        method = json.dumps
    return method(data, default=default, **kwargs)
