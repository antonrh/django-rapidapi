Django Rapid API extension.

*Inspired by [FastAPI](https://fastapi.tiangolo.com/).*

![tests](https://github.com/antonrh/django-rapidapi/workflows/tests/badge.svg)
[![codecov](https://codecov.io/gh/antonrh/django-rapidapi/branch/master/graph/badge.svg)](https://codecov.io/gh/antonrh/django-rapidapi)
[![Documentation Status](https://readthedocs.org/projects/django-rapidapi/badge/?version=latest)](https://django-rapidapi.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![version](https://img.shields.io/pypi/v/django-rapidapi.svg)](https://pypi.org/project/django-rapidapi/)
[![license](https://img.shields.io/pypi/l/django-rapidapi)](https://github.com/antonrh/django-rapidapi/blob/master/LICENSE)

---

## Quick start

*urls.py*

```python
from django.http import HttpRequest, HttpResponse
from django.urls import path

import rapidapi

api = rapidapi.RapidAPI()


@api.get("")
def hello(request: HttpRequest):
    return HttpResponse("Hello, RapidAPI")


urlpatterns = [
    path("api/", api.urls),
]
```
