from django.test import TestCase
from django.test.utils import override_settings

import myconf
import myprefixconf


class MyConfTest(TestCase):
    def test_setup(self):
        self.assertEqual(myconf.__name__, 'myconf')

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

    def test_all(self):
        before_import = set(locals().keys())
        from myconf import *
        after_import = set(locals().keys())
        self.assertEqual(
            sorted(after_import - before_import - {'before_import'}),
            ['BOOLEAN', 'INTEGER', 'LIST', 'METHOD', 'PROPERTY', 'STRING'])


class MyPrefixConfTest(TestCase):
    def test_setup(self):
        self.assertEqual(myprefixconf.__prefix__, 'FOO_BAR')

    def test_defaults(self):
        self.assertEqual(myprefixconf.BOOLEAN, True)

    @override_settings(FOO_BAR_BOOLEAN=False)
    def test_changes(self):
        self.assertEqual(myprefixconf.BOOLEAN, False)
