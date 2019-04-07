import os
import logging
from pathlib import Path

import yaml

FORMAT = '%(asctime)s %(levelname)s %(name)s - %(message)s'

logging.basicConfig(format=FORMAT)

logger = logging.getLogger("Yamz")
logger.setLevel(logging.INFO)


GLOBAL_KEY_NAME = 'global'


class YamzEnvironmentError(RuntimeError):
    pass


def _load_config(path: str) -> dict:
    if not Path(path).exists():
        raise YamzEnvironmentError("%s was not found!" % path)

    with open(path, 'r') as f:
        config = yaml.full_load(f.read())
    return config


def _parse_value(value: str) -> str:
    if value.startswith("$"):
        env_key = value[1:]
        env_value = os.environ.get(env_key)
        if not env_value:
            logger.info("Environment variable '{0}' was not found".format(env_key))
        return env_value
    return value


def _build(conf: dict) -> dict:
    parsed_conf = {}
    for k, v in conf.items():
        parsed_conf[k] = _parse_value(v)
    return parsed_conf


def _load(path: str, environment: str) -> dict:
    conf = _load_config(path)
    if environment not in conf:
        raise YamzEnvironmentError("environment %s does not exist "
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
            raise YamzEnvironmentError("Tried to access key `%s` before "
                                       "environment was loaded!" % key)
        return self._settings[key]
