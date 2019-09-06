import os
import pathlib
import unittest

from yamz import Yamz
from yamz.environment import YamzEnvironmentError


class YamzTestCase(unittest.TestCase):

    def setUp(self):
        base = os.path.abspath(pathlib.Path(__file__).parent)
        path = os.path.join(base, 'settings.yaml')
        self.yamz = Yamz(path)
        self.bad_environment = Yamz("/fake/path/settings.yaml")

    def test_file_not_found(self):
        with self.assertRaises(YamzEnvironmentError) as exc:
            self.bad_environment.load("global")

        self.assertEqual(exc.exception.args[0], "/fake/path/settings.yaml was not found!")

    def test_environment_not_loaded(self):
        with self.assertRaises(YamzEnvironmentError) as exc:
            _ = self.bad_environment.HOME

        self.assertEqual(exc.exception.args[0], "Tried to access key `%s` "
                                                "before environment was loaded!" % 'HOME')

    def test_load_environment(self):
        os.environ.setdefault("TEST", "/fake/home")
        self.yamz.load("global")
        self.assertEqual(self.yamz.TEST, "/fake/home")
        self.assertEqual(self.yamz.TEST_NUM, 12)
        self.assertEqual(self.yamz.YAMZ_ENV, 'global')
