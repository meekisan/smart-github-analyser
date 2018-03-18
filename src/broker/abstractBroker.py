from abc import ABC, abstractmethod

class AbstractBroker(ABC):

    @abstractmethod
    def connect(self):
        print("connect!")
    @abstractmethod
    def publish(self):
        print("publish")
    @abstractmethod
    def consume(self):
        print("consume")
