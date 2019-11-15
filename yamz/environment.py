import logging
import os
from pathlib import Path
from typing import Any, Dict, Iterable

import yaml

FORMAT = '%(asctime)s %(levelname)s %(name)s - %(message)s'

logging.basicConfig(format=FORMAT)

logger = logging.getLogger("Yamz")
logger.setLevel(logging.INFO)


class YamzEnvironmentError(RuntimeError):
    pass


def _load_config(path: str) -> Dict[str, Dict[str, Any]]:
    if not Path(path).exists():
        raise YamzEnvironmentError("%s was not found!" % path)

    with open(path, 'r') as f:
        config = yaml.full_load(f.read())
    return config


def _parse_value(value: str) -> str:
    if isinstance(value, str) and value.startswith("$"):
        env_key = value[1:]
        env_value = os.environ.get(env_key)
        if not env_value:
            logger.info("Environment variable '{0}' was not found".format(env_key))
        return env_value
    return value


def _build(conf) -> Dict[str, Any]:
    parsed_conf = {}
    for k, v in conf.items():
        parsed_conf[k] = _parse_value(v)
    return parsed_conf


def _load(path: str, environment: str) -> Dict:
    conf = _load_config(path)
    if environment not in conf:
        raise YamzEnvironmentError("environment %s does not exist "
                                   "in settings.yaml" % environment)

    defaults = {}
    if 'global' in conf:
        defaults = _build(conf['global'])

    env = _build(conf[environment])
    defaults.update(env)
    defaults['YAMZ_ENV'] = environment
    return defaults


class Yamz:
    def __init__(self, path: str):
        self.path = path
        self._loaded = False
        self._settings = {}

    def load(self, environment: str) -> None:
        settings = _load(self.path, environment)
        for k, v in settings.items():
            setattr(self, k, v)
            self._settings[k] = v
        self._loaded = True

    def get_setting_dict(self):
        return self._settings

    def __getattr__(self, key: str) -> str:
        if not self._loaded:
            raise YamzEnvironmentError("Tried to access key `%s` before "
                                       "environment was loaded!" % key)
        return self._settings[key]

    def __dir__(self) -> Iterable[str]:
        return [k for k in self.__dict__.keys() if k.isupper()]
