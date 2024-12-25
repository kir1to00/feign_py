import inspect
from functools import wraps
from typing import Optional
from urllib.parse import urljoin

import httpx

from core.interceptor.base import BaseInterceptor
from core.interceptor.default_interceptor import DefaultInterceptor
from core.router.router_factory import RouterFactory
from core.service_center.service_center_factory import ServiceCenterFactory
from enums.http_method import HttpMethod
from enums.router_enum import RouterEnum
from enums.service_center_enum import ServiceCenterEnum


class FeignApi(object):
    def __init__(self,
                 method: HttpMethod,
                 service_type: str = ServiceCenterEnum.DIRECT,
                 service_name: str = None,
                 url: str = None,
                 group_name: str = "DEFAULT_GROUP",
                 server_url: str = None,
                 router_strategy: str = RouterEnum.HASH,
                 name: str = None,
                 interceptor: BaseInterceptor = DefaultInterceptor(),
                 time_out: int = 60,
                 service_center_url: Optional[str] = None):
        """
        :param method 请求方法（GET|POST|PUT|DELETE）
        :param service_name 服务名称, 从注册中心获取服务
        :param group_name: str = None,
        :param server_url 服务地址 ,指定服务地址,如果不为空，则按此规则走
        :param name 服务名(描述)
        :param interceptor 请求与响应拦截器
        :param time_out 请求与响应拦截器
        """
        self.service_type = service_type
        self.url = url.lstrip('/')
        self.method = method
        self.group_name = group_name
        self.service_name = service_name
        self.server_url = server_url
        self.name = name
        self.interceptor = interceptor
        self.router_strategy = router_strategy
        self.time_out = time_out
        self.service_center_url = service_center_url

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            headers = {}
            params = {}
            body = {}
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            self.func_args = bound_args.arguments

            if self.method in [HttpMethod.GET, HttpMethod.DELETE]:
                # 将绑定后的参数添加到params字典中
                for name, value in bound_args.arguments.items():
                    params[name] = value

            elif self.method in [HttpMethod.POST, HttpMethod.PUT]:
                if len(args) > 0:
                    first_arg = args[0]
                    if hasattr(first_arg, '__dict__'):
                        body = first_arg.__dict__
                    else:
                        raise TypeError("First argument does not have __dict__ attribute")

            service_url = None
            if self.server_url is not None:
                service_url = self.server_url
            elif self.server_url is None and self.service_type != ServiceCenterEnum.DIRECT:
                service_info = ServiceCenterFactory.get_center(self.service_type).get_service(
                    service_url=self.service_center_url, service_name=self.service_name, group_name=self.group_name,
                    healthy_only=True)
                host = RouterFactory().get_service_url(self.router_strategy, service_info)
                service_url = urljoin(f"http://{host.ip}:{host.port}/", self.url)
            pr = self.interceptor.pre_request(method=self.method, headers=headers, params=params, body=body)
            with httpx.Client() as hpx:
                resp = hpx.request(method=self.method.value, url=service_url, params=pr.params, json=pr.body,
                                   headers=pr.headers,
                                   data=pr.data,
                                   timeout=self.time_out)
            func_result = self.interceptor.post_request(resp)
            return func_result

        return wrapper
