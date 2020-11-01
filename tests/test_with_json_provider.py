import json
import os
import pathlib
import tempfile
import unittest

from yamz import Yamz
from yamz.environment import YamzEnvironmentError
from yamz.providers.default import JsonProvider


class JsonProviderTestCase(unittest.TestCase):

    def setUp(self):
        base = os.path.abspath(pathlib.Path(__file__).parent)
        path = os.path.join(base, 'settings.json')
        self.yamz = Yamz(path, provider=JsonProvider)
        self.bad_environment = Yamz("/fake/path/settings.json")

    def test_file_not_found(self):
        with self.assertRaises(YamzEnvironmentError) as exc:
            self.bad_environment.load("global")

        self.assertEqual(
            exc.exception.args[0],
            "/fake/path/settings.json was not found!")

    def test_environment_not_loaded(self):
        with self.assertRaises(YamzEnvironmentError) as exc:
            _ = self.bad_environment.HOME

        self.assertEqual(
            exc.exception.args[0],
            "Tried to access key `%s` "
            "before environment was loaded!" % 'HOME')

    def test_load_environment(self):
        os.environ.setdefault("TEST", "/fake/home")
        self.yamz.load("global")
        self.assertEqual(self.yamz.TEST, "/fake/home")
        self.assertEqual(self.yamz.TEST_NUM, 12)
        self.assertEqual(self.yamz.YAMZ_ENV, 'global')

    def test_yamz_data_property(self):
        os.environ.setdefault("TEST", "/fake/home")
        self.yamz.load("global")
        self.assertIsNotNone(self.yamz.data)
        self.assertIsInstance(self.yamz.data, dict)

        expected_data = {
            'TEST': '/fake/home',
            'TEST_NUM': 12,
            'YAMZ_ENV': 'global'
        }

        self.assertEqual(self.yamz.data, expected_data)

    def test_write_to_file(self):
        temp_file_path = os.path.join(tempfile.gettempdir(), 'settings.json')

        with open(temp_file_path, 'w') as f:
            f.write(json.dumps({'global': {}}))

        yamz = Yamz(path=temp_file_path, provider=JsonProvider)
        yamz.load('global')

        yamz.write('TEST', 'TEST_VALUE')
        expected_data = {'TEST': 'TEST_VALUE', 'YAMZ_ENV': 'global'}

        self.assertEqual(yamz.data, expected_data)

        with open(temp_file_path, 'r') as f:
            self.assertEqual(json.loads(f.read()), {'global': {'TEST': 'TEST_VALUE'}})
