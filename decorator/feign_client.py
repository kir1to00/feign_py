from inspect import isclass
from typing import Optional

from core.cache.service_cache import ServiceCache
from core.interceptor.base import BaseInterceptor
from core.interceptor.default_interceptor import DefaultInterceptor
from functools import wraps

from core.service_center.service_center_factory import ServiceCenterFactory
from enums.router_enum import RouterEnum
from enums.service_center_enum import ServiceCenterEnum
from log.base import logger
from model.biz_schma import BizServerInfo


class FeignClient(object):
    def __init__(self,
                 service_type: str = ServiceCenterEnum.DIRECT,
                 service_name: str = None,
                 group_name: str = "DEFAULT_GROUP",
                 server_url: str = None,
                 router_strategy: str = RouterEnum.HASH,
                 name: str = None,
                 desc: str = None,
                 interceptor: BaseInterceptor = DefaultInterceptor(),
                 timeout: int = 60,
                 service_center_url: Optional[str] = None):
        """
        :param service_type 服务中心类型
        :param service_name 服务名
        :param server_url 服务地址
        :param group_name 分组名
        :param service_center_url 服务中心地址
        :param router_strategy 路由策略
        :param name 服务名
        :param desc 服务描述
        :param interceptor 拦截器
        :param timeout 最大超时时限
        """
        self.service_type = service_type
        self.service_name = service_name
        self.service_center_url = service_center_url
        self.server_url = server_url
        self.router_strategy = router_strategy
        self.name = name
        self.desc = desc
        self.group_name = group_name
        self.timeout = timeout
        self.interceptor = interceptor

    def __check__(self):
        if self.service_type == ServiceCenterEnum.DIRECT and self.server_url is None:
            logger.error('direct model must specify a service url')
            raise
        if self.service_type != ServiceCenterEnum.DIRECT and self.service_name is None:
            logger.error('server center model must specify a service_name')
            raise

    def __call__(self, cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            if not isclass(cls):
                raise Exception("@FeignClient can only work on classes")

            self.__check__()

            key = f"{cls.__module__}.{cls.__name__}"
            # 先从缓存中尝试加载配置
            biz_info = ServiceCache.get_service(key)

            # 初始化业务信息类
            biz_service_info = BizServerInfo()
            biz_service_info.desc = self.desc
            biz_service_info.name = self.name
            biz_service_info.interceptor = self.interceptor
            biz_service_info.time_out = self.timeout

            if biz_info is None:
                # 检查服务地址是否被指定 如果被指定则直接以指定地址配置
                if self.server_url is not None:
                    biz_service_info.server_url = self.server_url
                else:
                    # 如果服务中心名称不为直接连接，则从注册中心拉取配置
                    service_info = ServiceCenterFactory.get_center(self.service_type).get_service(
                        service_url=self.service_center_url, service_name=self.service_name, group_name=self.group_name,
                        healthy_only=True)
                    if service_info is not None:
                        biz_service_info.service_center_info = service_info
                if biz_service_info.server_url or biz_service_info.service_center_info:
                    ServiceCache.put_service(key, biz_service_info)
            return cls(*args, **kwargs)

        return wrapper
