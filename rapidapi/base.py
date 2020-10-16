from types import ModuleType
from typing import Callable, List, Optional, Tuple

from django.urls import path, include
from django.utils.functional import cached_property

from rapidapi.routing import Router


class RapidAPI:
    def __init__(self, *, namespace: Optional[str] = "rapidapi"):
        self.namespace = namespace
        self.router = Router(namespace=namespace)
        self.sub_routers: List[Tuple[Router, str]] = []

    @cached_property
    def urls(self) -> Tuple[ModuleType, Optional[str], Optional[str]]:
        urls = self.router.urls
        urls.extend(
            [
                path(prefix, include((router.urls, router.namespace)))
                for router, prefix in self.sub_routers
            ]
        )
        return include((urls, self.namespace))

    def add_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.router.add_route(path, endpoint, methods=methods, name=name)

    def add_router(self, router: Router, *, prefix: str = "") -> None:
        self.sub_routers.append((router, prefix))

    def route(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> Callable:
        return self.router.route(path, methods=methods, name=name)

    def get(
        self,
        path: str,
        *,
        name: Optional[str] = None,
    ) -> Callable:
        return self.router.get(path, name=name)

    def head(
        self,
        path: str,
        *,
        name: Optional[str] = None,
    ) -> Callable:
        return self.router.head(path, name=name)

    def post(
        self,
        path: str,
        *,
        name: Optional[str] = None,
    ) -> Callable:
        return self.router.post(path, name=name)

    def put(
        self,
        path: str,
        *,
        name: Optional[str] = None,
    ) -> Callable:
        return self.router.put(path, name=name)

    def patch(
        self,
        path: str,
        *,
        name: Optional[str] = None,
    ) -> Callable:
        return self.router.patch(path, name=name)

    def delete(
        self,
        path: str,
        *,
        name: Optional[str] = None,
    ) -> Callable:
        return self.router.delete(path, name=name)

    def options(
        self,
        path: str,
        *,
        name: Optional[str] = None,
    ) -> Callable:
        return self.router.options(path, name=name)

    def trace(
        self,
        path: str,
        *,
        name: Optional[str] = None,
    ) -> Callable:
        return self.router.trace(path, name=name)
