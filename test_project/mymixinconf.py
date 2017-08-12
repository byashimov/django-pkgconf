from pkgconf import Conf


class FooMixin(object):
    FOO = 'foo'

    @property
    def BAR(self):
        if self.FOO == 'foo':
            return 'original bar'
        return 'new bar'


class MyApp(FooMixin, Conf):
    BAZ = 'baz'
