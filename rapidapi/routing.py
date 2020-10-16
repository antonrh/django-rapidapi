import functools
from collections import defaultdict
from typing import Callable, Dict, Iterator, List, Optional, Tuple, Type, cast

from django.http import HttpResponse
from django.urls import path
from django.utils.functional import cached_property
from django.views import View


class Route:
    def __init__(
        self,
        path: str,
        endpoint: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.path = path
        self.endpoint = endpoint
        self.methods = methods or ["GET"]
        self.name = name

    @property
    def view_func(self) -> Callable:
        @functools.wraps(self.endpoint)
        def view(request, *args, **kwargs):
            return self.handle(request, *args, **kwargs)

        return view

    @property
    def view_method(self):
        def view(parent, request, *args, **kwargs):  # noqa
            return self.handle(request, *args, **kwargs)

        return view

    def handle(self, request, *args, **kwargs):
        response = self.endpoint(request, *args, **kwargs)
        return HttpResponse(response)


class Router:
    def __init__(self, *, namespace: Optional[str] = None) -> None:
        self.namespace = namespace
        self.routes: Dict[str, List[Route]] = defaultdict(list)

    @cached_property
    def urls(self):
        return [
            path(route, view=view, name=name)
            for route, view, name in self._iter_views()
        ]

    def add_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.routes[path].append(
            Route(path=path, endpoint=endpoint, methods=methods, name=name)
        )

    def route(
        self,
        path: str,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_route(path, func, methods=methods, name=name)
            return func

        return decorator

    def get(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["GET"], name=name)

    def head(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["HEAD"], name=name)

    def post(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["POST"], name=name)

    def put(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["PUT"], name=name)

    def patch(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["PATCH"], name=name)

    def delete(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["DELETE"], name=name)

    def options(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["OPTIONS"], name=name)

    def trace(self, path: str, *, name: Optional[str] = None) -> Callable:
        return self.route(path, methods=["TRACE"], name=name)

    def _iter_views(self) -> Iterator[Tuple[str, Callable, Optional[str]]]:
        for path, routes in self.routes.items():
            if len(routes) == 1:
                route = routes[0]
                view = route.view_func
                name = route.name
            else:
                view = cast(
                    Type[View],
                    type(
                        "RouterView",
                        (View,),
                        {
                            route.methods[0].lower(): route.view_method
                            for route in routes
                        },
                    ),
                ).as_view()
                name = None

            yield path, view, name
