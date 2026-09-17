# vpc-manager-api
This serverless api creates, retrieves AWS VPC components


## Introduction

- The idea is to build a serverless solution to interact with AWS VPC and related APIs to be able to provision and retrieve the VPC details.
- The following are the proposed services:
  - AWS API gateway: Single entry point for API management.
  - AWS Lambda: Compute layer running core logic.
  - AWS Dynamodb: To persists VPC details.
  - AWS Cognito: To manage user authentication.

### Architecture

- TBD: Architecture diagram

### User Journey

- User signs into cognito to get a JWT token.
- User calls the API gateway HTTP API using this token as a Authorization Bearer token.
- API Gateway authenticates and authorizes the request by contacting AWS Cognito via the gateway authorizers.
- Upon successful authentication, API Gateway invokes/triggers the lambda function.
- Upon unsuccessful authentication, API Gateway never triggers the lambda function and returns a `401` unauthorized response.
