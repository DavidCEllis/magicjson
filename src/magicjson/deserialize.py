"""
Convert from a magicjson serialized set of json data back to python objects
"""
import typing
from .registration import deserialize_register
from .exceptions import MissingDeserializerError


# Types natively serializable by the stdlib json moddule
native_serializable = typing.Union[None, bool, int, float, str, list, dict]


def loads(data: str, method=None, **kwargs):
    if method is None:
        import json
        method = json.loads

    pydata = method(data, **kwargs)
    return deserialize(pydata)


def deserialize(data: native_serializable):
    if isinstance(data, dict):
        if '_magicjson' in data:
            # First deserialize anything further down the chain
            converted_data = deserialize(data["contents"])
            # Then use the stored method to convert back to python
            deserializer_name = data["_deserializer"]
            if deserializer_name not in deserialize_register:
                raise MissingDeserializerError(
                    f"{data['_deserializer']} is not registered as a deserializer"
                )
            method = deserialize_register[deserializer_name]
            data = method(converted_data)
        else:
            for key in data.keys():
                data[key] = deserialize(data[key])
    elif isinstance(data, list):
        # Iterate over indices as we are replacing values
        for i in range(len(data)):
            data[i] = deserialize(data[i])
    return data
