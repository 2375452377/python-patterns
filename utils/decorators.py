#!/usr/bin/python
from functools import wraps


def need_attrs(*attrs):
    """检查方法是否有需要的属性，并属性不为空"""
    def _decorator(method):
        @wraps(method)
        def _inner(*args, **kwargs):
            obj = args[0]
            for a in attrs:
                if not getattr(obj, a, None):
                    raise ValueError(f'属性{a}不存在或值为空')
            return method(*args, **kwargs)

        return _inner

    return _decorator
