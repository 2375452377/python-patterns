#!/usr/bin/python
from utils.synchronized import synchronized


class SingletonMeta(type):
    """线程安全"""

    _instances = {}

    @synchronized
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


if __name__ == '__main__':
    import threading

    class A(metaclass=SingletonMeta):
        def __init__(self, name):
            self.name = name

    def task():
        print(A('1'))

    for i in range(100):
        threading.Thread(target=task).start()
