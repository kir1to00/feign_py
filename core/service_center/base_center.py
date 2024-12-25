from abc import ABC, abstractmethod


class BaseCenter(ABC):
    @abstractmethod
    def get_service(self, **kwargs):
        ...
