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
