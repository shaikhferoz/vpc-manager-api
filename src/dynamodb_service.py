"""DynamoDB service for storing VPC details."""
from datetime import datetime, timezone
import boto3


class DynamoDBService:
	"""Store VPC and subnet details in DynamoDB."""

	def __init__(self, table_name):
		self.table = boto3.resource('dynamodb').Table(table_name)

	def save_vpc(self, name, cidr_block, created_resources):
		"""Store a created VPC and its subnets."""
		item = {
			'id': created_resources['vpc_id'],
			'name': name,
			'cidr_block': cidr_block,
			'subnet_ids': created_resources['subnet_ids'],
			'created_at': datetime.now(timezone.utc).isoformat(),
		}
		print(f"Saving VPC details to DynamoDB: {item}")
		response = self.table.put_item(Item=item)
		print(f"DynamoDB put_item response: {response}")

	def get_vpc(self, vpc_id):
		"""Retrieve a VPC by its ID."""
		response = self.table.get_item(Key={'id': vpc_id})
		print(f"Retrieved VPC details from DynamoDB: {response.get('Item')}")
		return response.get('Item')
