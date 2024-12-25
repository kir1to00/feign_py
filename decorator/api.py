import inspect
from functools import wraps
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from core.cache.service_cache import ServiceCache
from core.router.router_factory import RouterFactory
from enums.http_method import HttpMethod
from log.base import logger


class Api(object):
    def __init__(self,
                 method: HttpMethod,
                 url: str,
                 name: str = None,
                 time_out: int = 60):
        """
        :param method: 请求方式
        :param url: 请求地址
        :param name: 接口名称
        :param time_out: 超时时限
        """
        self.method = method
        self.url = url.lstrip('/')
        self.name = name
        self.biz_info = None
        self.func = None
        self.func_args = None
        self.timeout = time_out

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not inspect.isfunction(func):
                raise Exception("@Api can only work on function")
            arg0 = args[0]
            module_cls_key = f"{type(arg0).__module__}.{type(arg0).__name__}" \
                if not isinstance(arg0, type) else f"{arg0.__module__}.{arg0.__name__}"

            biz_info = ServiceCache.get_service(module_cls_key)
            self.biz_info = biz_info
            self.func = func
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            self.func_args = bound_args.arguments
            result = self.__execute()
            return result

        return wrapper

    def __execute(self):
        biz_info = self.biz_info
        if biz_info.server_url is not None:
            if not biz_info.server_url.endswith('/'):
                biz_info.server_url += '/'
            service_url = urljoin(biz_info.server_url, self.url)
        elif biz_info.service_center_info is not None:
            host = RouterFactory().get_service_url(biz_info.router_strategy, biz_info.service_center_info)
            service_url = urljoin(f"http://{host.ip}:{host.port}/", self.url)
        else:
            logger.error("can't find any service url")
            raise
        headers = {}
        params = {}
        body = {}
        if self.method in [HttpMethod.GET, HttpMethod.DELETE]:
            for param_name, value in self.func_args.items():
                if param_name != 'self' and param_name != 'cls':  # 排除类或实例自身
                    params[param_name] = value
        elif self.method in [HttpMethod.POST, HttpMethod.PUT]:
            body_params = {k: v for k, v in self.func_args.items() if k not in ('self', 'cls')}
            if len(body_params) > 0:
                first_body_param = next(iter(body_params.values()))
                if isinstance(first_body_param, BaseModel):
                    body = first_body_param.dict()
                else:
                    body = first_body_param
        pr = biz_info.interceptor.pre_request(method=self.method, headers=headers, params=params, body=body)
        with httpx.Client() as hpx:
            resp = hpx.request(method=self.method.value, url=service_url, params=pr.params, json=pr.body,
                               headers=pr.headers,
                               data=pr.data,
                               timeout=self.timeout)
        func_result = biz_info.interceptor.post_request(resp)
        return func_result
