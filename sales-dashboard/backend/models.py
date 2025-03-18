from pydantic import BaseModel

class Sale(BaseModel):
    product_name: str
    sales_amount: float
    date: str  # ISO format

