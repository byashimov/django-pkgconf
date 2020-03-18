from django.test import SimpleTestCase
from django.test.utils import override_settings

import myconf
import mymixinconf
import myprefixconf


class MyConfTest(SimpleTestCase):
    def test_setup(self):
        self.assertEqual(myconf.__name__, 'myconf')

        # Generated prefix
        self.assertEqual(myconf.__prefix__, 'MYAPP')

    def test_defaults(self):
        self.assertEqual(myconf.LIST, [])
        self.assertEqual(myconf.STRING, 'test')
        self.assertEqual(myconf.INTEGER, 0)
        self.assertEqual(myconf.BOOLEAN, True)
        self.assertEqual(myconf.METHOD('baz!'), 'test baz!')
        self.assertEqual(myconf.PROPERTY, 'test baz!')

    @override_settings(MYAPP_STRING='modified', MYAPP_INTEGER=1,
                       MYAPP_METHOD=lambda self, string: 'new ' + string,
                       MYAPP_PROPERTY=property(lambda self: 'new baz'))
    def test_changes(self):
        self.assertEqual(myconf.STRING, 'modified')
        self.assertEqual(myconf.INTEGER, 1)
        self.assertEqual(myconf.METHOD('baz'), 'new baz')
        self.assertEqual(myconf.PROPERTY, 'new baz')

    def test_unknown(self):
        with self.assertRaises(AttributeError):
            myconf.UNKNOWN

    def test_monkeypatching(self):
        from django.conf import settings
        settings.MYAPP_STRING = 'monkey'
        self.assertEqual(myconf.STRING, 'monkey')
        # Property returns the new value
        self.assertEqual(myconf.PROPERTY, 'monkey baz!')

        # Reverse
        with self.assertRaises(AttributeError):
            myconf.STRING = 'banana'

        # Be aware of this
        myconf.LIST.append('boo!')
        self.assertEqual(myconf.LIST, ['boo!'])

    def test_function(self):
        self.assertEqual(myconf.METHOD.__name__, 'METHOD')
        self.assertEqual(myconf.METHOD.__doc__, 'Method docstring')


class MyPrefixConfTest(SimpleTestCase):
    def test_setup(self):
        self.assertEqual(myprefixconf.__prefix__, 'FOO_BAR')

    def test_defaults(self):
        self.assertEqual(myprefixconf.BOOLEAN, True)

    @override_settings(FOO_BAR_BOOLEAN=False)
    def test_changes(self):
        self.assertEqual(myprefixconf.BOOLEAN, False)


class MyMixinConfTest(SimpleTestCase):
    def test_defaults(self):
        self.assertEqual(mymixinconf.FOO, 'foo')
        self.assertEqual(mymixinconf.BAR, 'original bar')

    @override_settings(MYAPP_FOO='new foo', MYAPP_BAZ='new baz')
    def test_changes(self):
        self.assertEqual(mymixinconf.FOO, 'new foo')
        self.assertEqual(mymixinconf.BAR, 'new bar')
        self.assertEqual(mymixinconf.BAZ, 'new baz')
