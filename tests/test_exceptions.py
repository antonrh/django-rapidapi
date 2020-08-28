from http import HTTPStatus

from rapidapi.exceptions import APIException


def test_api_exception_detail():
    exc = APIException(HTTPStatus.BAD_REQUEST)

    assert exc.detail == "Bad Request"
