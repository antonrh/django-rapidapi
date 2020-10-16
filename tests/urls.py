from django.urls import path

from tests.api import api

urlpatterns = [
    path("api/", api.urls),
]
