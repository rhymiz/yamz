import os
from pathlib import Path

from yaml import load

GLOBAL_KEY_NAME = 'global'


def _load_config(path: str) -> dict:
    if not Path(path).exists():
        raise EnvironmentError("%s was not found!" % path)

    with open(path, 'r') as f:
        config = load(f.read())
    return config


def _parse_value(key: str, value: str) -> str:
    if value.startswith("$"):
        return os.environ.get(key, value)
    return value


def _build(conf: dict) -> dict:
    parsed_conf = {}
    for k, v in conf.items():
        parsed_conf[k] = _parse_value(k, v)
    return parsed_conf


def _load(path: str, environment: str) -> dict:
    conf = _load_config(path)
    if environment not in conf:
        raise EnvironmentError("environment %s does not exist "
                               "in settings.yaml" % environment)

    defaults = {}
    if GLOBAL_KEY_NAME in conf:
        defaults = _build(conf[GLOBAL_KEY_NAME])

    env = _build(conf[environment])
    defaults.update(env)
    return defaults


class Environment(object):
    def __init__(self, path: str):
        self.path = path
        self._loaded = False
        self._settings = {}

    def load(self, environment: str) -> None:
        self._loaded = True
        self._settings = _load(self.path, environment)

    def __getattr__(self, key: str) -> str:
        if not self._loaded:
            raise EnvironmentError("Tried to access key `%s` before "
                                   "environment was loaded!" % key)
        return self._settings[key]
