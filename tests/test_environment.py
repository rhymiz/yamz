import os
import unittest

from yamz import Environment
from yamz.environment import YamzEnvironmentError


class EnvironmentTestCase(unittest.TestCase):

    def setUp(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, 'settings.yaml')
        self.environment = Environment(path)
        self.bad_environment = Environment("/fake/path/settings.yaml")

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
        self.environment.load("global")
        print(self.environment._settings)
        self.assertEqual(self.environment.TEST, "/fake/home")
