from django.urls import path

from tests.endpoints import ProductsEndpoint

urlpatterns = [path("", ProductsEndpoint.as_view(), name="products")]
