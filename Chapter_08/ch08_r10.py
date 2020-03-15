"""Python Cookbook 2nd ed.

Chapter 8, recipe 10, Writing recursive generator functions with the yield from statement
"""
from typing import List, Dict, Union, Any, Iterator, Optional


JSON_DOC = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

Node_Id = Union[str, int]


def find_path(
    value: Any, node: JSON_DOC, path: Optional[List[Node_Id]] = None
) -> Iterator[List[Node_Id]]:
    if path is None:
        path = []
    if isinstance(node, dict):
        for key in sorted(node.keys()):
            yield from find_path(value, node[key], path + [key])
    elif isinstance(node, list):
        for index in range(len(node)):
            yield from find_path(value, node[index], path + [index])
    else:  # str, int, float, bool, None
        if node == value:
            yield path


import math


def factor_list(x: int) -> List[int]:
    limit = int(math.sqrt(x) + 1)
    for n in range(2, limit):
        q, r = divmod(x, n)
        if r == 0:
            return [n] + factor_list(q)
    return [x]


def factor_iter(x: int) -> Iterator[int]:
    limit = int(math.sqrt(x) + 1)
    for n in range(2, limit):
        q, r = divmod(x, n)
        if r == 0:
            yield n
            yield from factor_iter(q)
            return
    yield x


document = {
    "field": "value1",
    "field2": "value",
    "array": [{"array_item_key1": "value"}, {"array_item_key2": "array_item_value2"}],
    "object": {"attribute1": "value", "attribute2": "value2"},
}

test_find_value1 = """
>>> list(find_path('value1', document))
[['field']]
"""

test_find_array_item_value2 = """
>>> list(find_path('array_item_value2', document))
[['array', 1, 'array_item_key2']]
"""

test_find_object_value2 = """
>>> list(find_path('value2', document))
[['object', 'attribute2']]
"""

test_find_value = """
>>> list(find_path('value', document))
[['array', 0, 'array_item_key1'], ['field2'], ['object', 'attribute1']]
"""

test_factor_list_factor_iter = """
>>> factor_list(255255)
[3, 5, 7, 11, 13, 17]
>>> list(factor_iter(255255))
[3, 5, 7, 11, 13, 17]
>>> from collections import Counter
>>> Counter(factor_iter(384))
Counter({2: 7, 3: 1})
"""

__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
