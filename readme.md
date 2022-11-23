# MagicJSON #
Easy handling of JSON serialization and deserialization for python objects.

If you are just interested in making basic serialization easier you might
want to look [here](https://github.com/DavidCEllis/magicjson/blob/main/plain_serializer/jsonregister.py).

## Motivation ##
While working on PrefabClasses I ran into the issue of how to add handling 
of JSON encoding for the derived classes. Defining a 'default' function allowed 
for easy recursive serialization but became awkward when then handling other 
objects without built-in serialization.

This module provides a `JSONRegister` class that can be used to collect
methods to serialize and reconstruct data to/from JSON. 

The `JSONRegister` class accepts 1 argument which is jsonlib which should
be a JSON module such as the stdlib module that provides `dumps` and `loads` 
functions where the `dumps` function **must** accept a default parameter
in the same manner as the stdlib `dumps`. If these methods are called
withtout providing a json module, it will lazily fall back to the stdlib.

Alternatively the class also provides `default` and `reconstruct` methods.
`default` is intended to be provided to a `dump` or `dumps` function.
`reconstruct` is intended to be run on the result of a `load` or `loads` function.


## Examples ##

Example 1: Path objects

```python
from pathlib import Path

from magicjson import JSONRegister

register = JSONRegister()

register.register_cls_encoder(cls=Path, method=str)
register.register_cls_decoder(cls=Path, method=Path)

test_example = {
    "test1": Path("test1"),
    "test2": Path("test2")
}

test_dump = register.dumps(test_example, indent=2)
test_recover = register.loads(test_dump)

print("JSON Output:")
print(test_dump)
print("Recovered Dict:")
print(test_recover)
```

Output:
```
JSON Output:
{
  "test1": {
    "_magicjson": "v0.0.2a",
    "_deserializer": "Path",
    "contents": "test1"
  },
  "test2": {
    "_magicjson": "v0.0.2a",
    "_deserializer": "Path",
    "contents": "test2"
  }
}
Recovered Dict:
{'test1': PosixPath('test1'), 'test2': PosixPath('test2')}
```

Example 2: Dataclasses

```python
from dataclasses import dataclass, fields

from magicjson import JSONRegister

register = JSONRegister()


@dataclass
class Coordinate:
    x: float
    y: float


@dataclass
class Circle:
    radius: float
    origin: Coordinate


@register.cls_encoder(Circle)
@register.cls_encoder(Coordinate)
def plain_dict(dc):
    # Don't use dataclasses.asdict as it will recurse and break the Coordinate object
    return {f.name: getattr(dc, f.name) for f in fields(dc)}


@register.cls_decoder(Circle)
def decode_circle(data):
    return Circle(**data)


@register.cls_decoder(Coordinate)
def decode_coordinate(data):
    return Coordinate(**data)


basic_circle = Circle(radius=1.0, origin=Coordinate(0.0, 0.0))

circle_json = register.dumps(basic_circle, indent=2)
circle_restored = register.loads(circle_json)

print("JSON Output:")
print(circle_json)
print("Reconstructed Data:")
print(circle_restored)
```

Output:
```
JSON Output:
{
  "_magicjson": "v0.0.2a",
  "_deserializer": "Circle",
  "contents": {
    "radius": 1.0,
    "origin": {
      "_magicjson": "v0.0.2a",
      "_deserializer": "Coordinate",
      "contents": {
        "x": 0.0,
        "y": 0.0
      }
    }
  }
}
Reconstructed Data:
Circle(radius=1.0, origin=Coordinate(x=0.0, y=0.0))
```