# MagicJSON #
Easy handling of JSON serialization/deserialization of python objects. 

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

The idea then was to make a module that would allow simple decorators to declare
that a function was the method for a class to be serialized. These can then be
used to generate a 'default' function that covers all of the objects.

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
    "_magicjson": "0.0.1a",
    "_class": "Path",
    "_alias": "Path",
    "contents": "test1"
  },
  "test2": {
    "_magicjson": "0.0.1a",
    "_class": "Path",
    "_alias": "Path",
    "contents": "test2"
  }
}
(test_recover == test_example)=True
```
