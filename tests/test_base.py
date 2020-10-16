import pytest
from django.http import HttpResponse

from rapidapi.base import RapidAPI
from rapidapi.routing import Router


@pytest.fixture()
def api():
    return RapidAPI()


def test_add_route(api: RapidAPI):
    api.add_route("test", endpoint=lambda r: HttpResponse(""))

    assert len(api.router.routes) == 1


def test_add_router(api: RapidAPI):
    router = Router()
    api.add_router(router, prefix="sub")

    assert api.sub_routers == [(router, "sub")]
