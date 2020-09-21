import os
from pathlib import Path
from typing import Any, Dict

import yaml

from yamz.errors import YamzEnvironmentError
from yamz.logger import logger
from yamz.providers.base import BaseProvider


class YamlProvider(BaseProvider):
    def __init__(self, *args, **kwargs):
        self._data = {}
        super().__init__(*args, **kwargs)

    def setup(self) -> None:
        self._data = self._load(self.path, self.environment)

    def write(self, key, data):
        raise NotImplemented("can't write to a YAML file")

    def read(self, key):
        return self._data.get(key)

    def _open(self, path: str) -> Dict[str, Dict[str, Any]]:
        if not Path(path).exists():
            raise YamzEnvironmentError("%s was not found!" % path)

        with open(path, 'r') as f:
            config = yaml.full_load(f.read())
        return config

    def _parse_value(self, value: str) -> str:
        if isinstance(value, str) and value.startswith("$"):
            env_key = value[1:]
            env_value = os.environ.get(env_key)
            if not env_value:
                logger.info("Environment variable %s was not found" % env_key)
            return env_value
        return value

    def _build(self, conf) -> Dict[str, Any]:
        parsed_conf = {}
        for k, v in conf.items():
            parsed_conf[k] = self._parse_value(v)
        return parsed_conf

    def _load(self, path: str, environment: str) -> Dict:
        conf = self._open(path)

        if environment not in conf:
            raise YamzEnvironmentError("environment %s does not exist in %s" % (environment, path))

        defaults = {}
        if 'global' in conf:
            defaults = self._build(conf['global'])

        env = self._build(conf[environment])
        defaults.update(env)
        defaults['YAMZ_ENV'] = environment
        return defaults
