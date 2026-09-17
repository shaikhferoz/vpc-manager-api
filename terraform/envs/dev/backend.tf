terraform {
  backend "s3" {
    bucket       = "awslabs-terraform-state-433306737932"
    key          = "dev/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}