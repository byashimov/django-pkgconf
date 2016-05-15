import sys
from functools import partial, update_wrapper
from django.utils import six


def proxy(attr, default):
    def wrapper(self):
        # It has to be most recent,
        # to override settings in tests
        from django.conf import settings
        value = getattr(settings, attr, default)
        if callable(value):
            func = partial(value, self)
            return update_wrapper(func, value)
        elif isinstance(value, property):
            return value.__get__(self)
        return value
    return property(wrapper)


class ConfMeta(type):
    def __new__(mcs, name, bases, attrs):
        prefix = attrs.get('__prefix__', name.upper()) + '_'
        for attr, value in attrs.items():
            if not attr.startswith('__'):
                attrs[attr] = proxy(prefix + attr, value)

        # Ready to build
        cls = super(ConfMeta, mcs).__new__(mcs, name, bases, attrs)

        # Sets non-abstract conf as module
        abstract = attrs.get('__abstract__', False)
        if not abstract:
            # http://mail.python.org/pipermail/python-ideas/2012-May/
            # 014969.html
            ins = cls()
            ins.__name__ = ins.__module__
            sys.modules[ins.__module__] = ins
        return cls


class Conf(six.with_metaclass(ConfMeta)):
    __abstract__ = True
