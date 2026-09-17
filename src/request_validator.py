"""Validation helpers for API request bodies."""

def validate_vpc_request(request_body):
    """Return an error message when a VPC request is invalid."""
    required_fields = ('name', 'cidr_block', 'subnets')
    missing_fields = [
        field for field in required_fields if field not in request_body
    ]
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}"

    if not isinstance(request_body['subnets'], list) or not request_body['subnets']:
        return "subnets must be a non-empty list"

    return None