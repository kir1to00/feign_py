from typing import Any, Optional, Dict

from pydantic import BaseModel, Field

from enums.http_method import HttpMethod


class RequestParams(BaseModel):
    method: HttpMethod
    headers: Optional[Dict[str, Any]] = None
    params: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = Field(default=None)
    body: Any = None
