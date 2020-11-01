import json
import os
from typing import Any, Dict

from yamz.errors import YamzEnvironmentError
from yamz.logger import logger
from yamz.providers.base import BaseProvider


class YamlProvider(BaseProvider):
    """
    Provider for reading configurations
    from a JSON file.
    """

    def __init__(self, *args, **kwargs):
        self._data = {}
        super().__init__(*args, **kwargs)

    def setup(self) -> None:
        self._validate_path()
        self._data = self._load(self.path, self.environment)

    def write(self, key: str, data: Any):
        raise NotImplementedError(
            "writing to or updating a YAML file "
            "is currently unsupported.",
        )

    def read(self, key: str):
        return self._data.get(key)

    def get_data(self) -> Dict[str, Any]:
        return self._data

    def _open(self, path: str) -> Dict[str, Dict[str, Any]]:
        try:
            import yaml
        except ImportError:
            raise YamzEnvironmentError(
                "pip install PyYAML to use YamlProvider",
            )

        with open(path, 'r') as f:
            config = yaml.full_load(f.read())
        return config

    def _parse_value(self, value: str) -> str:
        if isinstance(value, str) and value.startswith("$"):
            env_key = value[1:]
            env_value = os.environ.get(env_key)
            if not env_value:
                logger.warning("Environment variable %s was not found" % env_key)
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


class JsonProvider(YamlProvider):
    """
    Provider for reading configurations
    from a JSON file.
    """

    def write(self, key: str, data: Any) -> None:
        current = self._open(self.path)
        current[self.environment][key] = data

        with open(self.path, 'w') as f:
            logger.info("writing to file: %s" % self.path)
            f.write(json.dumps(current))

        self._data[key] = data

    def _open(self, path: str) -> Dict[str, Dict[str, Any]]:
        self._validate_path()
        with open(path, 'r') as f:
            config = json.loads(f.read())
        return config
