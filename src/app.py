"""Lambda handler for the VPC Manager API."""
import json
import os

from dynamodb_service import DynamoDBService
from vpc_service import VPCService

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
    http_method = event.get('requestContext', {}).get('http', {}).get('method')
    if http_method == 'GET':
        vpc_id = event.get('pathParameters', {}).get('vpc_id')

        if not vpc_id:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Expected path /vpcs/{vpc_id}"}),
            }

        vpc = dynamodb_service.get_vpc(vpc_id)

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

    request_body = json.loads(event.get("body") or "{}")

    # TBD: Add some validators on the request body:

    # Create the VPC and its subnets using the VPCService:
    created_resources = vpc_service.create_vpc_with_subnet(
        request_body['name'],
        request_body['cidr_block'],
        request_body['subnets'],
    )

    # Persist the created VPC and subnet details in DynamoDB using the DynamoDBService:
    dynamodb_service.save_vpc(
        request_body['name'],
        request_body['cidr_block'],
        created_resources,
    )

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