from pkgconf import Conf


class MyApp(Conf):
    LIST = []
    STRING = 'test'
    INTEGER = 0
    BOOLEAN = True

    def METHOD(self, string):
        """Method docstring"""
        return '{} {}'.format(self.STRING, string)

    @property
    def PROPERTY(self):
        return self.STRING + ' baz!'
