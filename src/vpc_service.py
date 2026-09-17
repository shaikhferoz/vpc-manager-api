"""EC2 VPC Service module for managing VPCs and related resources."""
import boto3

class VPCService:
    """Service class for managing VPCs and related resources."""

    def __init__(self):
        """Initialize the VPCService with a Boto3 EC2 client."""
        self.ec2_client = boto3.client('ec2')

    def create_vpc(self, cidr_block, name):
        """Create a new VPC with the specified CIDR block."""
        response = self.ec2_client.create_vpc(
            CidrBlock=cidr_block,
            TagSpecifications=[
                {
                    'ResourceType': 'vpc',
                    'Tags': [{'Key': 'Name', 'Value': name}],
                }
            ],
        )
        print(f"Created VPC with ID: {response['Vpc']['VpcId']}")
        vpc_id = response['Vpc']['VpcId']
        return vpc_id

    def create_subnet(self, vpc_id, name, cidr_block, availability_zone):
        """Create a new subnet in the specified VPC."""
        response = self.ec2_client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr_block,
            AvailabilityZone=availability_zone,
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [{'Key': 'Name', 'Value': name}],
                }
            ],
        )
        subnet_id = response['Subnet']['SubnetId']
        print(f"Created Subnet with ID: {subnet_id} in VPC: {vpc_id}")
        return subnet_id

    def create_vpc_with_subnet(self, name, cidr_block, subnets):
        """Create a VPC and its requested subnets."""
        vpc_id = self.create_vpc(cidr_block, name)
        subnet_ids = []
        for subnet in subnets:
            subnet_id = self.create_subnet(
                vpc_id,
                subnet['name'],
                subnet['cidr_block'],
                subnet['az'],
            )
            subnet_ids.append(subnet_id)
        created_resources = {
            'vpc_id': vpc_id,
            'subnet_ids': subnet_ids,
        }
        print(f"Created VPC and Subnets: {created_resources}")
        return created_resources
