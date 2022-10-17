from typing import *
import re
import json
Fn = Callable
K = TypeVar('K')
V = TypeVar('V')
to_snake_case: Fn[[str], str] = lambda camel: re.sub(r'(?<!^)(?=[A-Z])', '_', camel).lower()
tags = set([])
def snake_case_key(key: K)->K:
    if isinstance(key, str):
        return to_snake_case(key)
    return key

def snake_case_dict(d: Dict[K,V])->Dict[K,V]:
    if not isinstance(d, dict):
        return d
    ret: Dict[K,V] = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v: V = snake_case_dict(v)
        if isinstance(v, list):
            v = [snake_case_dict(x) for x in v]
            if k == "tags":
                for tag in v:
                    tags.add(tag)
        ret[snake_case_key(k)] = v 
    return ret

