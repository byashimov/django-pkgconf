from django.test import TestCase
from django.test.utils import override_settings

import myconf


class PkgConfTest(TestCase):
    def test_setup(self):
        self.assertEqual(myconf.__name__, 'myconf')

    def test_defaults(self):
        self.assertEqual(myconf.LIST, [])
        self.assertEqual(myconf.STRING, 'test')
        self.assertEqual(myconf.INTEGER, 0)
        self.assertEqual(myconf.BOOLEAN, True)
        self.assertEqual(myconf.LAMBDA('foo'), 'foo')
        self.assertEqual(myconf.FUNCTION('bar'), 'bar')

    @override_settings(MYAPP_STRING='modified', MYAPP_INTEGER=1)
    def test_changes(self):
        self.assertEqual(myconf.STRING, 'modified')
        self.assertEqual(myconf.INTEGER, 1)

    def test_unknown(self):
        with self.assertRaises(AttributeError):
            myconf.DEBUG

    def test_monkeypatching(self):
        from django.conf import settings
        settings.MYAPP_STRING = 'monkey'
        self.assertEqual(myconf.STRING, 'monkey')

        # Reverse
        with self.assertRaises(AttributeError):
            myconf.STRING = 'banana'

        # Be aware of this
        myconf.LIST.append('boo!')
        self.assertEqual(myconf.LIST, ['boo!'])

    def test_function(self):
        self.assertEqual(myconf.FUNCTION.__name__, 'foo')
        self.assertEqual(myconf.FUNCTION.__doc__, 'Foo function')
