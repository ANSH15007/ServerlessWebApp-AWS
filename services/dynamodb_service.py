import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
import os
import json
from datetime import datetime

class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.products_table = self.dynamodb.Table(os.environ['PRODUCTS_TABLE'])
        self.orders_table = self.dynamodb.Table(os.environ['ORDERS_TABLE'])
        self.users_table = self.dynamodb.Table(os.environ['USERS_TABLE'])

    def get_product(self, product_id: str):
        try:
            response = self.products_table.get_item(
                Key={'product_id': product_id}
            )
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting product: {e}")
            return None

    def create_product(self, product_data: dict):
        product_data['created_at'] = datetime.now().isoformat()
        try:
            self.products_table.put_item(Item=product_data)
            return product_data
        except ClientError as e:
            print(f"Error creating product: {e}")
            return None

    def create_order(self, order_data: dict):
        order_data['created_at'] = datetime.now().isoformat()
        try:
            self.orders_table.put_item(Item=order_data)
            return order_data
        except ClientError as e:
            print(f"Error creating order: {e}")
            return None

    def get_user_orders(self, user_id: str):
        try:
            response = self.orders_table.query(
                IndexName='user_id-index',
                KeyConditionExpression='user_id = :uid',
                ExpressionAttributeValues={':uid': user_id}
            )
            return response.get('Items', [])