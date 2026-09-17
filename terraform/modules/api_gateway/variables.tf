variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}

variable "project_prefix" {
  description = "Prefix for project resources"
  type        = string
  default     = "vpc-manager"
}

variable "lambda_function_arn" {
  description = "The ARN of the Lambda function to integrate with the API Gateway."
  type        = string
}

variable "cognito_app_client_id" {
  description = "The ID of the Cognito App Client for JWT validation."
  type        = string
}

variable "cognito_issuer_url" {
  description = "The OIDC issuer URL used by API Gateway authorizer for JWT validation."
  type        = string
}