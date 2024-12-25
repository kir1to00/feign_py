from abc import ABC, abstractmethod

from model.center_schema import BaseServiceInfo


class Router(ABC):
    @abstractmethod
    def select(self, si: BaseServiceInfo):
        ...
