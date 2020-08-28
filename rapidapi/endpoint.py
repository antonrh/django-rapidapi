# import inspect
import inspect
import json
import logging
from http import HTTPStatus
from typing import Any, Callable, List, Optional

import pydantic
from django.core.exceptions import PermissionDenied
from django.db import connection, transaction
from django.http import Http404, HttpRequest, HttpResponse
from django.views import View

from rapidapi.exceptions import APIException
from rapidapi.response import JsonResponse

logger = logging.getLogger(__name__)


def empty():
    pass


class APIEndpoint(View):
    request: HttpRequest
    decorators: List[Callable] = []

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._json: Optional[Any] = empty

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        try:
            return self.handle(request, *args, **kwargs)
        except Exception as exc:
            return self.handle_exception(exc)

    def handle(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        method = request.method.lower()
        operation: Callable = getattr(self, method, None)

        # Handle not allowed http method
        if not (operation and method in self.http_method_names):
            raise self.http_method_not_allowed(request, *args, **kwargs)

        signature = inspect.signature(operation)

        for parameter in signature.parameters.values():
            if (
                parameter.annotation
                and parameter.name not in kwargs
                and (issubclass(parameter.annotation, pydantic.BaseModel) or True)
            ):
                kwargs[parameter.name] = pydantic.parse_obj_as(
                    parameter.annotation, obj=self.json()
                )

        response = operation(*args, **kwargs)

        if not isinstance(response, HttpResponse):
            response = JsonResponse(content=response)

        return response

    def json(self) -> Any:
        if self._json is empty:
            try:
                self._json = json.loads(self.request.body)
            except (TypeError, ValueError) as exc:
                raise APIException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                    detail=f"Invalid JSON body: {exc}",
                )
        return self._json

    def handle_exception(self, exc: Exception):
        if isinstance(exc, Http404):
            exc = APIException(status_code=HTTPStatus.NOT_FOUND)
        elif isinstance(exc, PermissionDenied):
            exc = APIException(status_code=HTTPStatus.FORBIDDEN)
        elif isinstance(exc, pydantic.ValidationError):
            exc = APIException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=exc.errors()
            )

        if isinstance(exc, APIException):
            if isinstance(exc.detail, (dict, list)):
                data = exc.detail
            else:
                data = {"detail": exc.detail}

            set_rollback()

            return JsonResponse(data, status=exc.status_code, headers=exc.headers)
        raise exc

    def http_method_not_allowed(self, request: HttpRequest, *args, **kwargs) -> Any:
        logger.warning(
            f"Method Not Allowed ({request.method}): {request.path}",
            extra={"status_code": HTTPStatus.METHOD_NOT_ALLOWED, "request": request},
        )
        allowed_methods = self._allowed_methods()
        raise APIException(
            status_code=HTTPStatus.METHOD_NOT_ALLOWED,
            headers={"Allow": ", ".join(allowed_methods)},
        )


def set_rollback():
    atomic_requests = connection.settings_dict.get("ATOMIC_REQUESTS", False)
    if atomic_requests and connection.in_atomic_block:
        transaction.set_rollback(True)
