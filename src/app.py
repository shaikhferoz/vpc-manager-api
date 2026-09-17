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
    request_body = json.loads(event.get("body") or "{}")

    # TBD: Add some validators on the request body:

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