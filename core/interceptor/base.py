from abc import ABC, abstractmethod
from typing import Any

from httpx import Response

from enums.http_method import HttpMethod


class BaseInterceptor(ABC):
    @abstractmethod
    def pre_request(self,
                    method: HttpMethod,
                    headers: dict = None,
                    params: dict = None,
                    data: dict = None,
                    body: Any = None,
                    **kwargs):
        ...

    @abstractmethod
    def post_request(self, resp: Response):
        ...
