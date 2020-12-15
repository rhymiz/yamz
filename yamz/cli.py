import os

from yamz import Yamz
from yamz.errors import YamzEnvironmentError
from yamz.logger import logger
from yamz.utils import safe_import_resolver


def main(action: str, key: str, data: str, environment: str, path: str = None, provider: str = None):
    config = {'path': path}

    provider_ref = provider or os.getenv('YAMZ_DEFAULT_PROVIDER')
    provider_class = None
    if provider_ref:
        provider_class = safe_import_resolver(provider_ref)

    if provider_class:
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
