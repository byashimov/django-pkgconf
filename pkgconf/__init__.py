import sys
from functools import partial, update_wrapper
from django.utils import six


def proxy(attr, default):
    def wrapper(self):
        # It has to be the most recent
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
        cls = type.__new__(mcs, name, bases, attrs)
        abstract = attrs.pop('__abstract__', False)
        if abstract:
            return cls

        prefix = attrs.pop('__prefix__', name.upper())
        fields = {
            key: proxy(prefix + '_' + key, attrs.get(key, getattr(cls, key)))
            for key in dir(cls) if not key.startswith('_')
        }
        attrs.update(fields, __all__=tuple(fields), __prefix__=prefix)
        new_cls = type.__new__(mcs, name, bases, attrs)

        # Sets non-abstract conf as a module
        # http://mail.python.org/pipermail/python-ideas/2012-May/
        # 014969.html
        ins = new_cls()
        ins.__name__ = ins.__module__
        sys.modules[ins.__module__] = ins
        return new_cls


class Conf(six.with_metaclass(ConfMeta)):
    __abstract__ = True
