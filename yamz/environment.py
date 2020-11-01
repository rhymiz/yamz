from typing import Any, Optional, Type

from yamz.errors import YamzEnvironmentError
from yamz.providers.base import BaseProvider
from yamz.providers.default import YamlProvider


class Yamz:
    def __init__(self, path: str = None,
                 provider: Type[BaseProvider] = YamlProvider) -> None:
        assert issubclass(provider, BaseProvider)

        self.path = path
        self._loaded = False
        self._provider: Optional[BaseProvider] = None
        self._provider_class = provider

    @property
    def data(self):
        return self._provider.get_data()

    def load(self, environment: str) -> None:
        provider = self._provider_class(environment=environment, path=self.path)
        self._provider = provider
        self._loaded = True

    def write(self, key: str, data: Any) -> Optional[Any]:
        return self._provider.write(key=key, data=data)

    def __getattr__(self, item: str) -> Optional[Any]:
        if not self._loaded:
            raise YamzEnvironmentError(
                "Tried to access key `%s` before "
                "environment was loaded!" % item)
        return self._provider.read(item)
