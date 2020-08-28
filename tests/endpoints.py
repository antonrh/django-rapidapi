from pydantic import BaseModel

from rapidapi import APIEndpoint, Body


class Product(BaseModel):
    id: int
    name: str


class ProductsEndpoint(APIEndpoint):
    def get(self):
        return {"success": True}

    def post(self, product: Product = Body()):
        return product.dict()
