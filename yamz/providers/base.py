from abc import abstractmethod


class BaseProvider:
    """
    Base class for building providers.
    """

    def __init__(self, environment, path=None):
        self.path = path
        self.environment = environment

        self.setup()

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
