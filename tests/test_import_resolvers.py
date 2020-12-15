import unittest

from yamz.providers.default import JsonProvider
from yamz.utils import import_resolver, safe_import_resolver


class ImportResolverTestCase(unittest.TestCase):
    def test_import_resolver_correctly_returns_provider_class(self):
        klass = None
        import_failed = False
        try:
            klass = import_resolver('yamz.providers.default.JsonProvider')
        except ImportError:
            import_failed = True

        self.assertFalse(import_failed)
        self.assertEqual(klass, JsonProvider)

    def test_safe_import_resolver_correctly_returns_provider_class(self):
        klass = None
        import_failed = False
        try:
            klass = safe_import_resolver('yamz.providers.default.JsonProvider')
        except ImportError:
            import_failed = True

        self.assertFalse(import_failed)
        self.assertEqual(klass, JsonProvider)

    def test_import_resolver_raises_import_error_on_import_failure(self):
        with self.assertRaises(ImportError):
            import_resolver('path.to.BogusProvider')

    def test_safe_import_resolver_returns_none_on_import_failure(self):
        klass = safe_import_resolver('path.to.BogusProvider')
        self.assertIsNone(klass)

    def test_import_resolver_assertion_fails_when_attribute_not_exist_in_module(self):
        with self.assertRaises(TypeError):
            import_resolver('yamz.providers.default.BogusProvider')
