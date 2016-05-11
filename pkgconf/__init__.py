import sys

from django.utils import six


def proxy(attr, default):
    def wrapper(self):
        # It has to be most recent,
        # to override settings in tests
        from django.conf import settings
        return getattr(settings, attr, default)
    return property(wrapper)


class ConfMeta(type):
    def __new__(mcs, name, bases, attrs):
        prefix = name.upper() + '_'
        for attr, value in attrs.items():
            if not attr.startswith('__'):
                attrs[attr] = proxy(prefix + attr, value)

        abstract = attrs.pop('__abstract__', False)
        cls = super(ConfMeta, mcs).__new__(mcs, name, bases, attrs)

        if not abstract:
            # http://mail.python.org/pipermail/python-ideas/2012-May/
            # 014969.html
            ins = cls()
            ins.__name__ = ins.__module__
            sys.modules[ins.__module__] = ins
        return cls


class Conf(six.with_metaclass(ConfMeta)):
    __abstract__ = True
