from pkgconf import Conf


class MyConf(Conf):
    __prefix__ = 'FOO_BAR'

    BOOLEAN = True
