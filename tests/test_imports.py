# flake8: noqa

from django.test import SimpleTestCase

BEFORE_IMPORT = set(locals().keys())
from myconf import *
AFTER_IMPORT = set(locals().keys())


class ImportsTest(SimpleTestCase):
    def test_import_star(self):
        self.assertEqual(
            sorted(AFTER_IMPORT - BEFORE_IMPORT - {'BEFORE_IMPORT'}),
            ['BOOLEAN', 'INTEGER', 'LIST', 'METHOD', 'PROPERTY', 'STRING'])

    def test_import_by_name(self):
        # Proves variable does not exist
        with self.assertRaises(NameError):
            self.assertTrue(BOOLEAN)

        # Now it's good
        from myprefixconf import BOOLEAN
        self.assertTrue(BOOLEAN)
