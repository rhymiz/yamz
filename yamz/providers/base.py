from abc import abstractmethod
from pathlib import Path

from yamz.errors import YamzEnvironmentError


class BaseProvider:
    """
    Base class for building providers.
    """

    def __init__(self, environment, path=None):
        self.path = path
        self.environment = environment

        self.setup()

    def _validate_path(self):
        if not Path(self.path).exists():
            raise YamzEnvironmentError("%s was not found!" % self.path)

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def read(self, key):
        pass

    @abstractmethod
    def write(self, key, data):
        pass

    def get_data(self):
        """
        Optionally return a dictionary of
        all the loaded settings.
        """
        pass
