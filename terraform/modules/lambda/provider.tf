# Module level provider requirements.  No provider block is needed here since the module will inherit the provider from the root module.
terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
    archive = {
        source = "hashicorp/archive"
        version = "~> 2.4"
    }
  }
}