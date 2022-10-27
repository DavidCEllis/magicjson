# MagicJSON #
Easy handling of JSON serialization and deserialization for python objects.

If you are just interested in making basic serialization easier you might
want to look [here](https://gist.github.com/DavidCEllis/df51bbdc8d2668d1e5b291c7367a9c1e).

I thought this would use magic __ methods but decorators were more flexible
and now this might need a better name.

If you want your JSON decoding to be fast this module is not for you.
If you want to be able to round-trip python objects to JSON and back
this might be for you.

## Motivation ##
While working on PrefabClasses I ran into the issue of how to add handling of 
JSON encoding for the derived classes. Defining a 'default' function allowed
for easy recursive serialization but became awkward when then handling other
objects without built-in serialization.

For instance: if an attribute of the prefab is a Path, then the JSON serializer
needs to know how to serialize both the prefab and the Path object as neither
has a default serialization method. 

The `json.dumps` function provides a way to define either a deserializaton class 
or a default method, however defining a default method will override a default 
provided by the class and the function only has 1 argument so a default method
would need to know how to serialize every potential method.

Looking at `dataclasses` it seems the 
[solution](https://github.com/python/cpython/blob/3e335f2c0de9b7fab542a18d603f5bbdb1fb2ef3/Lib/dataclasses.py#L1242) 
used there is to create an asdict function that would do all of the work necesary 
to create a serializable form.
This involves recursing through the contents of the class and checking for 
tuples/namedtuples/lists/dicts specifically and would not handle arbitrary
container types.

The idea then was to make a module that would allow simple decorators to declare
that a function was the method for a class to be serialized. These can then be
used to generate a 'default' function that covers all of the objects.
Working this way the json serializer does the traversal for us and will convert
each object using the appropriate function from the register.

It then seemed interesting to find a way to make the deserialization/loads method
return the original objects instead of just a plain dictionary.

## Example Usage ##

Code:
```python
from pathlib import Path

from magicjson import dumps, loads, serializer, deserializer

@serializer(cls=Path)
def serialize_path(pth: Path) -> str:
    return str(pth)

@deserializer(cls=Path)
def deserialize_path(pth: str) -> Path:
    return Path(pth)

test_example = {
    "test1": Path("test1"),
    "test2": Path("test2")
}

test_dump = dumps(test_example, indent=2)
test_recover = loads(test_dump)

print(test_dump)
print(f"{(test_recover == test_example)=}")
```

Output:
```
{
  "test1": {
    "_magicjson": "0.1.0",
    "_deserializer": "Path",
    "contents": "test1"
  },
  "test2": {
    "_magicjson": "0.1.0",
    "_deserializer": "Path",
    "contents": "test2"
  }
}
(test_recover == test_example)=True
```

## Usage with DataClasses #

```python
from dataclasses import dataclass

from magicjson import dumps, loads
from magicjson.tools.stdlib_serializers import register_path_serializer, register_dataclass_serializer
from magicjson.tools.dataclasses import magicjson_dataclass

# builtin dataclass and path serializers
register_dataclass_serializer()
register_path_serializer()


@magicjson_dataclass
@dataclass
class Coordinate:
    x: float
    y: float


@magicjson_dataclass
@dataclass
class Circle:
    radius: float
    origin: Coordinate


basic_circle = Circle(radius=1.0, origin=Coordinate(0.0, 0.0))
circle_json = dumps(basic_circle, indent=2)
circle_restored = loads(circle_json)

print(circle_json)
print(f"{(circle_restored == basic_circle)=}")
```

Output:
```
{
  "_magicjson": "0.1.0",
  "_deserializer": "dataclass",
  "contents": {
    "radius": 1.0,
    "origin": {
      "_magicjson": "0.1.0",
      "_deserializer": "dataclass",
      "contents": {
        "x": 0.0,
        "y": 0.0,
        "__class__.__name__": "Coordinate"
      }
    },
    "__class__.__name__": "Circle"
  }
}
(circle_restored == basic_circle)=True
```

