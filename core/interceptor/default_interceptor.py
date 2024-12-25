from typing import Any, cast, List, NamedTuple, Optional

from httpx import Response

from core.entity.request_params import RequestParams
from core.entity.response import FeignRemoteResponse
from core.interceptor.base import BaseInterceptor
from enums.http_method import HttpMethod
from enums.http_status_code import HttpStatusCode, BizCode, HttpMessage


class ByteEncoding(NamedTuple):
    """File encoding as the NamedTuple."""

    encoding: Optional[str]
    """The encoding of the file."""
    confidence: float
    """The confidence of the encoding."""
    language: Optional[str]
    """The language of the file."""


class DefaultInterceptor(BaseInterceptor):
    def pre_request(self, method: HttpMethod, headers: dict = None, params: dict = None, data: dict = None,
                    body: Any = None, **kwargs):
        if headers.get('Content-Type') is None:
            headers['Content-Type'] = "application/json"
        rq = RequestParams(
            method=method,
            headers=headers,
            params=params,
            data=data,
            body=body
        )
        return rq

    @staticmethod
    def __read_and_detect(file_byte: bytes) -> List[dict]:
        import chardet
        return cast(List[dict], chardet.detect_all(file_byte))

    def post_request(self, resp: Response):
        http_status = HttpStatusCode(resp.status_code)
        if http_status == HttpStatusCode.SUCCESS:
            encodings = self.__read_and_detect(resp.content)
            if all(encoding["encoding"] is None for encoding in encodings):
                raise RuntimeError("Could not detect encoding")
            enc = [ByteEncoding(**enc) for enc in encodings if enc["encoding"] is not None][0]
            return FeignRemoteResponse(code=BizCode.SUCCESS, message=HttpMessage.SUCCESS,
                                       data=resp.content.decode(enc.encoding))
        elif http_status == HttpStatusCode.BAD_REQUEST:
            return FeignRemoteResponse(code=BizCode.ERROR, message=HttpMessage.BAD_REQUEST)
        elif http_status == HttpStatusCode.FORBIDDEN:
            return FeignRemoteResponse(code=BizCode.ERROR, message=HttpMessage.FORBIDDEN)
        elif http_status == HttpStatusCode.NOT_FOUND:
            return FeignRemoteResponse(code=BizCode.ERROR, message=HttpMessage.NOT_FOUND)
        elif http_status == HttpStatusCode.METHOD_NOT_ALLOW:
            return FeignRemoteResponse(code=BizCode.ERROR, message=HttpMessage.METHOD_NOT_ALLOW)
        elif http_status == HttpStatusCode.SERVER_ERROR:
            return FeignRemoteResponse(code=BizCode.ERROR, message=HttpMessage.SERVER_ERROR)
        elif http_status == HttpStatusCode.BAD_GATEWAY:
            return FeignRemoteResponse(code=BizCode.ERROR, message=HttpMessage.BAD_GATEWAY)
        elif http_status == HttpStatusCode.SERVER_UNAVAILABLE:
            return FeignRemoteResponse(code=BizCode.ERROR, message=HttpMessage.SERVER_UNAVAILABLE)
        elif http_status == HttpStatusCode.GATEWAY_TIMEOUT:
            return FeignRemoteResponse(code=BizCode.ERROR, message=HttpMessage.GATEWAY_TIMEOUT)
        else:
            return FeignRemoteResponse(code=BizCode.ERROR, message=HttpMessage.UNKNOWN_ERROR)
