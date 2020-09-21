from typing import Any, Optional, Type

from yamz.errors import YamzEnvironmentError
from yamz.providers.base import BaseProvider
from yamz.providers.default import YamlProvider


class Yamz:
    def __init__(self, path: str = None, provider: Type[BaseProvider] = YamlProvider) -> None:
        assert issubclass(provider, BaseProvider)

        self.path = path
        self._loaded = False
        self._provider: Optional[BaseProvider] = None
        self._provider_class = provider

    def load(self, environment: str) -> None:
        provider = self._provider_class(environment=environment, path=self.path)
        self._provider = provider
        self._loaded = True

    def __getattr__(self, item: str) -> Optional[Any]:
        if not self._loaded:
            raise YamzEnvironmentError(
                "Tried to access key `%s` before "
                "environment was loaded!" % item)
        return self._provider.read(item)
