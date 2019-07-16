#!/usr/bin/python
# Copyright © 2012-13 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version. It is provided for
# educational purposes and is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import abc
import collections
import errno
import functools
import os
import sys


def coroutine(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        generator = function(*args, **kwargs)
        next(generator)
        return generator

    return wrapper


if sys.version_info[:2] < (3, 3):
    def remove_if_exists(filename):
        try:
            os.remove(filename)
        except OSError as err:
            if err.errno != errno.ENOENT:
                raise
else:
    def remove_if_exists(filename):
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass  # All other exceptions are passed to the caller

# Thanks to Nick Coghlan for these!
if sys.version_info[:2] >= (3, 3):
    def has_methods(*methods):
        """
        1）可以像抽象类基类那样检查接口是否匹配
        2）可以像"动态类型(duck typing)"那样只要有对应的方法就可以视为匹配
        """
        def decorator(base):
            def __subclasshook__(cls, subclass):
                if cls is base:
                    attributes = collections.ChainMap(*(superclass.__dict__ for superclass in subclass.__mro__))
                    # 判断待检查类是否有 methods 里的方法，如果有就视待检查类是基类的子类
                    if all(method in attributes for method in methods):
                        return True
                # 如果它返回 NotImplemented，则使用通常的机制继续子类检查。
                return NotImplemented

            base.__subclasshook__ = classmethod(__subclasshook__)
            return base

        return decorator
else:
    def has_methods(*methods):
        def decorator(base):
            def __subclasshook__(cls, subclass):
                if cls is base:
                    needed = set(methods)
                    for superclass in subclass.__mro__:
                        for method in needed.copy():
                            if method in superclass.__dict__:
                                needed.discard(method)
                        if not needed:
                            return True
                return NotImplemented

            base.__subclasshook__ = classmethod(__subclasshook__)
            return base

        return decorator


# Thanks to Nick Coghlan for this!
class Requirer(metaclass=abc.ABCMeta):

    # Since we have rules for adding new expected attributes, we *do*
    # perform the check for subclasses
    @classmethod
    def __subclasshook__(cls, subclass):
        methods = set()
        for superclass in subclass.__mro__:
            if hasattr(superclass, 'required_methods'):
                methods |= set(superclass.required_methods)
        attributes = collections.ChainMap(*(superclass.__dict__ for superclass in cls.__mro__))
        if all(method in attributes for method in methods):
            return True
        return NotImplemented


def report(message='', error=False):
    if len(message) >= 70 and not error:
        message = message[:67] + '...'
    sys.stdout.write('\r{:70}{}'.format(message, '\n' if error else ''))
    sys.stdout.flush()
