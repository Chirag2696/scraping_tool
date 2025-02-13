# models/product.py
from pydantic import BaseModel, Field

class Product(BaseModel):
    product_title: str = Field(..., example="Toothbrush")
    product_price: float = Field(..., example=9.99)
    path_to_image: str = Field(..., example="/images/toothbrush.jpg")
