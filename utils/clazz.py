#!/usr/bin/python
def get_subclasses(cls):
    """获取所有子类"""
    for subclass in cls.__subclasses__():
        yield from subclass.__subclasses__()
        yield subclass
