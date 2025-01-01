from abc import ABC, abstractmethod


class IFullRepository(ABC):
    @abstractmethod
    def load(self):
        pass

    def save(self, data=None):
        pass

    def get(self, key, default=None):
        pass

    def set(self, key, value):
        pass

    def delete(self, key):
        pass
