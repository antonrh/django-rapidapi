import pytest
from django.test import Client


def test_api_route(client: Client):
    response = client.get("/api/route")

    assert response.status_code == 200
    assert response.content == b"ROUTE:GET"

    response = client.post("/api/route")

    assert response.status_code == 200
    assert response.content == b"ROUTE:POST"


@pytest.mark.parametrize(
    "method,content",
    [
        ("GET", b"GET"),
        ("HEAD", b""),
        ("POST", b"POST"),
        ("PUT", b"PUT"),
        ("PATCH", b"PATCH"),
        ("DELETE", b"DELETE"),
        ("OPTIONS", b"OPTIONS"),
        ("TRACE", b"TRACE"),
    ],
)
def test_api_method(client: Client, method: str, content: bytes):
    response = client.generic(method, "/api/")

    assert response.status_code == 200
    assert response.content == content
