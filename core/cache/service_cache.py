from typing import Union

from core.cache.core import SERVICES_INFO_CACHE
from model.center_schema import BaseServiceInfo


class ServiceCache:
    """
    服务缓存
    """

    @staticmethod
    def get_service(key) -> Union[BaseServiceInfo, None]:
        if key in SERVICES_INFO_CACHE:
            return SERVICES_INFO_CACHE[key]
        return None

    @staticmethod
    def put_service(key, si: BaseServiceInfo):
        SERVICES_INFO_CACHE[key] = si
        return True

    @staticmethod
    def del_service(key):
        del SERVICES_INFO_CACHE[key]
        return True

    @staticmethod
    def clear_service():
        SERVICES_INFO_CACHE.clear()
        return True
