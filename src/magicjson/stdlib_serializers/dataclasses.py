"""
Dataclass register in order to deserialize dataclasses.
"""
from magicjson import serializer, deserializer
from magicjson.exceptions import RegistrationError

dataclass_register: dict[str, type] = {}


def magicjson_dataclass(cls):
    if cls.__name__ in dataclass_register:
        raise RegistrationError(f"Dataclass with name {cls.__name__} already in dataclass registry")
    dataclass_register[cls.__name__] = cls
    return cls


def register_dataclass_serializer():
    """
    Register the default dataclass serializer with magicjson
    """
    # Lazy import
    from dataclasses import is_dataclass, fields

    @serializer(identifier=is_dataclass, deserializer_name='dataclass')
    def serialize_dataclass(dc):
        class_name = dc.__class__.__name__

        if class_name not in dataclass_register:
            raise RegistrationError(
                f"Dataclass {class_name} not in serialization registry.",
                "@magicjson_dataclass decorator must be applied to class definition."
            )

        data = {
            f.name: getattr(dc, f.name) for f in fields(dc)
        }
        data['__class__.__name__'] = class_name

        # Keep track of fields that are not in INIT
        data['_exclude_init_fields'] = [f.name for f in fields(dc) if not f.init]

        return data

    @deserializer(name='dataclass')
    def deserialize_dataclass(data):
        class_name = data.pop('__class__.__name__')
        if class_name in dataclass_register:
            cls = dataclass_register[class_name]
        else:
            raise RegistrationError(
                f"Could not find dataclass matching {class_name} to deserialize.",
                "@magicjson_dataclass decorator must be applied to class definition."
            )
        exclude_fields = data.pop('_exclude_init_fields')
        for fieldname in exclude_fields:
            del data[fieldname]
        return cls(**data)
