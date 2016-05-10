from pkgconf import Conf


def foo(bar):
    """Foo function"""
    return bar


class MyApp(Conf):
    LIST = []
    STRING = 'test'
    INTEGER = 0
    BOOLEAN = True
    LAMBDA = lambda x: x
    FUNCTION = foo
