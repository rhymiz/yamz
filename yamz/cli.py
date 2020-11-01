import importlib
from typing import Type

from yamz import Yamz
from yamz.errors import YamzEnvironmentError
from yamz.logger import logger
from yamz.providers.base import BaseProvider


def import_resolver(module_path: str) -> Type[BaseProvider]:
    """
    Takes a string reference to a class and returns
    an actual Python class.
    """

    split_path = module_path.split('.')
    klass = split_path[-1]
    package = '.'.join(split_path[:-1])
    module = importlib.import_module(package)
    provider_class = getattr(module, klass)
    assert issubclass(provider_class, BaseProvider)
    return provider_class


def main(action: str, key: str, data: str, environment: str, path: str = None, provider: str = None):
    config = {'path': path}
    if provider:
        provider_class = import_resolver(provider)
        config.update({'provider': provider_class})

    yamz = Yamz(**config)
    try:
        yamz.load(environment=environment)
    except YamzEnvironmentError as e:
        logger.error('\n'.join(e.args))
        return None

    if action == 'read':
        result = getattr(yamz, key)
        if not result:
            logger.error("key %s was not found" % key)
        else:
            print(result)

    if action == 'write':
        try:
            yamz.write(key=key, data=data)
        except NotImplementedError:
            logger.error(
                "write operations have not been "
                "implemented for this provider",
            )
