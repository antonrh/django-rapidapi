from typing import Any, Optional, Union

from django.http.response import HttpResponse, JsonResponse as DjangoJsonResponse
from django.utils.encoding import force_bytes


class Response(HttpResponse):
    def __init__(
        self,
        content: Union[str, bytes] = b"",
        headers: Optional[dict] = None,
        *args,
        **kwargs
    ):
        super().__init__(force_bytes(content), *args, **kwargs)

        set_headers(self, headers)


class JsonResponse(DjangoJsonResponse):
    def __init__(self, content: Any, headers: Optional[dict] = None, **kwargs):
        kwargs["safe"] = False
        super().__init__(content, **kwargs)

        set_headers(self, headers)


def set_headers(response: HttpResponse, headers: Optional[dict] = None) -> None:
    if headers:
        for name, value in headers.items():
            response[name] = value
