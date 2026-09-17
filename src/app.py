"""Lambda handler for the VPC Manager API."""
import json
import logging
import os

from botocore.exceptions import ClientError
from dynamodb_service import DynamoDBService
from request_validator import validate_vpc_request
from vpc_service import VPCService

# Initialize application-wide logging for Lambda and its service modules.
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Create an instance of the VPCService to manage VPCs and subnets:
vpc_service = VPCService()
dynamodb_service = DynamoDBService(os.environ['DYNAMODB_TABLE_NAME'])


def lambda_handler(event, context):
    """Handle incoming requests to the VPC Manager API.
    Sample body for creating a VPC with subnets:
    {
        "name": "my-vpc",
        "cidr_block": "10.0.0.0/16",
        "subnets" : [
            {
                "name": "subnet-1",
                "cidr_block": "10.0.1.0/24",
                "az": "us-east-1a"
            },
            {
                "name": "subnet-2",
                "cidr_block": "10.0.2.0/24",
                "az": "us-east-1b"
            }
        ]
    }
    """
    # Retrieval handler: load a stored VPC using the API Gateway path parameter.
    http_method = event.get('requestContext', {}).get('http', {}).get('method')
    logger.info(f"Received {http_method} request")

    if http_method == 'GET':
        vpc_id = event['pathParameters']['vpc_id']
        try:
            vpc = dynamodb_service.get_vpc(vpc_id)
        except ClientError as error:
            logger.exception(f"Unable to retrieve VPC: {error}")
            retrieve_error_response = {
                "statusCode": 500,
                "body": json.dumps({"error": "Unable to retrieve VPC"}),
            }
            return retrieve_error_response

        if not vpc:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "VPC not found"}),
            }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(vpc),
        }

    # Creation handler: validate the request before creating any AWS resources.
    # Validate the incoming request body for creating a VPC and its subnets:
    request_body = json.loads(event.get("body") or "{}")
    
    validation_error = validate_vpc_request(request_body)
    if validation_error:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": validation_error}),
        }

    # Create the VPC and its subnets, then persist their details in DynamoDB.
    try:
        created_resources = vpc_service.create_vpc_with_subnet(
            request_body['name'],
            request_body['cidr_block'],
            request_body['subnets'],
        )

        dynamodb_service.save_vpc(
            request_body['name'],
            request_body['cidr_block'],
            created_resources,
        )
    except ClientError as error:
        logger.exception(f"Unable to create VPC: {error}")
        create_error_response = {
            "statusCode": 500,
            "body": json.dumps({"error": "Unable to create VPC"}),
        }
        return create_error_response

    # Build the API response with the created VPC and subnet IDs:
    api_response = {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "vpc_id": created_resources['vpc_id'],
            "subnet_ids": created_resources['subnet_ids'],
        }),
    }
    return api_response