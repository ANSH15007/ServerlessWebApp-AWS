from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class Product(BaseModel):
    product_id: str
    name: str
    description: str
    price: Decimal
    stock: int
    category: str
    created_at: datetime
    updated_at: Optional[datetime]

class Order(BaseModel):
    order_id: str
    user_id: str
    products: List[dict]
    total_amount: Decimal
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

class User(BaseModel):
    user_id: str
    email: str
    name: str
    created_at: datetime
    last_login: Optional[datetime]