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

variable "source_dir" {
  description = "The source directory for the Lambda function code"
  type        = string
}

variable "dynamodb_table_name" {
  description = "The DynamoDB table used to store VPC details"
  type        = string
}

variable "dynamodb_table_arn" {
  description = "The ARN of the DynamoDB table used to store VPC details"
  type        = string
}