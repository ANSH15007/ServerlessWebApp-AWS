provider "aws" {
  region = "us-east-1"
}

# DynamoDB Tables
resource "aws_dynamodb_table" "products" {
  name           = "products"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "product_id"
  
  attribute {
    name = "product_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "orders" {
  name           = "orders"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "order_id"
  
  attribute {
    name = "order_id"
    type = "S"
  }
  
  attribute {
    name = "user_id"
    type = "S"
  }

  global_secondary_index {
    name               = "user_id-index"
    hash_key           = "user_id"
    projection_type    = "ALL"
  }
}

# Lambda Functions
resource "aws_lambda_function" "api" {
  filename         = "../package/api_handler.zip"
  function_name    = "ecommerce-api"
  role            = aws_iam_role.lambda_role.arn
  handler         = "api_handler.handler"
  runtime         = "python3.9"

  environment {
    variables = {
      PRODUCTS_TABLE = aws_dynamodb_table.products.name
      ORDERS_TABLE   = aws_dynamodb_table.orders.name
    }
  }
}

# API Gateway
resource "aws_apigatewayv2_api" "main" {
  name          = "ecommerce-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id = aws_apigatewayv2_api.main.id
  name   = "prod"
  auto_deploy = true
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "api" {
  enabled = true
  
  origin {
    domain_name = "${aws_apigatewayv2_api.main.id}.execute-api.${var.region}.amazonaws.com"
    origin_id   = "ApiGateway"
    
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }
  
  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD", "OPTIONS"]
    target_origin_id       = "ApiGateway"
    viewer_protocol_policy = "redirect-to-https"
    
    forwarded_values {
      query_string = true
      cookies {
        forward = "all"
      }
    }
  }
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  
  viewer_certificate {
    cloudfront_default_certificate = true
  }
}