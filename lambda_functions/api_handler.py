from fastapi import FastAPI, HTTPException
from mangum import Mangum
from services.dynamodb_service import DynamoDBService
from models.product import Product, Order
from typing import List
import os

app = FastAPI()
db_service = DynamoDBService()

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    product = db_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products")
async def create_product(product: Product):
    result = db_service.create_product(product.dict())
    if not result:
        raise HTTPException(status_code=500, detail="Failed to create product")
    return result

@app.post("/orders")
async def create_order(order: Order):
    result = db_service.create_order(order.dict())
    if not result:
        raise HTTPException(status_code=500, detail="Failed to create order")
    return result

@app.get("/users/{user_id}/orders")
async def get_user_orders(user_id: str):
    orders = db_service.get_user_orders(user_id)
    return orders

# AWS Lambda handler
handler = Mangum(app)