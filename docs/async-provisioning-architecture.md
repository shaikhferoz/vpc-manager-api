# Asynchronous VPC Provisioning 

## The Proposed Flow

- Asynchronous model by splitting our single lambda into 2 or more lambdas:
    - Request Lambda: This lambda registers the task of creation AWS resources in SQS and in DynamoDB.
    - Worker Lambda: This lambda reads from SQS Queue and provisions the infrastructure. It then writes the current status back to DynamoDB.
- Introduce SQS Queue for decoupling the architecture.
- Integrate AWS Step functions for implementing coordinated steps and custom retry/cleanup logic till the provisioning in complete.
- Enhance code logic to include custom validations:
    - Before creating resources, check whether the resource ID is already present in the DynamoDB.
    - Validate if the request body contains the correct JSON schema.

```text
Phase 1: Register the Task:
Client
  |
  | POST /vpcs
  v
API Gateway -> Request Lambda
                  |
                  +--> Save job as QUEUED in DynamoDB
                  +--> Send job to SQS
                  +--> Return 202 Accepted

Phase 2: Asynchronous task execution:
SQS -> Worker Lambda -> Create VPC and subnets in EC2
                     -> Update job in DynamoDB


Client -> GET /vpcs/jobs/{job_id} -> Read status from DynamoDB
```

## Why Return `202 Accepted`?

`202 Accepted` means the request was valid and accepted, but the work is not finished yet. The client receives a job ID instead of waiting for the VPC to be created.

```http
POST /vpcs
```

The request body remains the same as the current API. The request Lambda should return immediately:

```http
202 Accepted
Location: /vpcs/jobs/job-123
```

```json
{
  "job_id": "job-123",
  "status": "QUEUED",
  "status_url": "/vpcs/jobs/job-123"
}
```

The client must not expect `vpc_id` or `subnet_ids` in the initial response because those resources may not exist yet.

### Check provisioning status

```http
GET /vpcs/jobs/{job_id}
```

Queued or running:

```json
{
  "job_id": "job-123",
  "status": "IN_PROGRESS"
}
```

Successful:

```json
{
  "job_id": "job-123",
  "status": "SUCCEEDED",
  "vpc_id": "vpc-0123456789abcdef0",
  "subnet_ids": [
    "subnet-0123456789abcdef0",
    "subnet-0123456789abcdef1"
  ]
}
```

Failed:

```json
{
  "job_id": "job-123",
  "status": "FAILED",
  "message": "VPC provisioning failed"
}
```

A separate `GET /vpcs/{vpc_id}` resource query can remain for retrieving completed VPC details.
