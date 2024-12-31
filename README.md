# Serverless E-commerce Application

This is a serverless e-commerce application built with AWS services and Python. The application provides a scalable backend for handling product management, orders, and customer data processing.

## Architecture

- **API Layer**: AWS API Gateway + Lambda
- **Database**: Amazon DynamoDB
- **CDN**: CloudFront
- **ETL Processing**: AWS Glue
- **Authentication**: AWS Cognito (not implemented in this example)

## Key Features

- Product management
- Order processing
- Customer segmentation
- ETL pipeline for data processing
- Global content delivery with CloudFront

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure AWS credentials:
   ```bash
   aws configure
   ```

3. Deploy infrastructure:
   ```bash
   cd terraform
   terraform init
   terraform apply
   ```

4. Deploy Lambda functions:
   ```bash
   # Package and deploy using your preferred deployment method
   # (AWS SAM, Serverless Framework, or manual deployment)
   ```

## API Endpoints

- GET /products/{product_id} - Get product details
- POST /products - Create new product
- POST /orders - Create new order
- GET /users/{user_id}/orders - Get user's orders

## Performance Features

- DynamoDB auto-scaling
- CloudFront caching
- Lambda concurrency handling
- ETL optimization