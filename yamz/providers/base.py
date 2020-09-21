from abc import abstractmethod


class BaseProvider:
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
