from core.router import HashRouter, RobinRouter, RandomsRouter
from enums.router_enum import RouterEnum
from log.base import logger
from model.center_schema import BaseServiceInfo


class RouterFactory:
    def get_service_url(self, router_type: str, si: BaseServiceInfo):
        if router_type == RouterEnum.ROBIN:
            return RobinRouter().select(si)
        elif router_type == RouterEnum.RANDOM:
            return RandomsRouter().select(si)
        elif router_type == RouterEnum.HASH:
            return HashRouter().select(si)
        else:
            logger.error(f"Class: {self.__class__.__name__}, Method: get_service_url, "
                         f"Error: Unsupported router type: {router_type},Use Hash Router")
            return HashRouter().select(si)
