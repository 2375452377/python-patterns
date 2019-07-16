#!/usr/bin/python
from threading import RLock


def synchronized(func):
    func.__lock__ = RLock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func
