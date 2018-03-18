from abc import ABC, abstractmethod

class AbstractBackend(ABC):

    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def insert_one(self):
        pass
    @abstractmethod
    def close(self):
        pass
