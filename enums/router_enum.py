from core.router import HashRouter, RobinRouter, RandomsRouter
from enums.base import BaseEnum


class RouterEnum(BaseEnum):
    HASH = HashRouter
    ROBIN = RobinRouter
    RANDOM = RandomsRouter
