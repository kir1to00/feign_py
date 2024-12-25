from enums.base import BaseEnum


class HttpStatusCode(BaseEnum):
    SUCCESS = 200
    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOW = 405
    SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVER_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class HttpMessage(BaseEnum):
    SUCCESS = "success"
    BAD_REQUEST = "bad_request"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not found"
    METHOD_NOT_ALLOW = "method not allow"
    SERVER_ERROR = "server error"
    BAD_GATEWAY = "bad gateway"
    SERVER_UNAVAILABLE = "server unavailable"
    GATEWAY_TIMEOUT = "gateway timeout"
    UNKNOWN_ERROR = "unknown error"


class BizCode(BaseEnum):
    SUCCESS = 0
    ERROR = -1
