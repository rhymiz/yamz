import importlib
from typing import Optional, Type

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
    provider_class = getattr(module, klass, None)
    assert issubclass(provider_class, BaseProvider)
    return provider_class


def safe_import_resolver(module_path: str) -> Optional[Type[BaseProvider]]:
    try:
        return import_resolver(module_path)
    except ImportError:
        logger.warning("Unable to import provider '%s', falling back to default." % module_path)
        return None
