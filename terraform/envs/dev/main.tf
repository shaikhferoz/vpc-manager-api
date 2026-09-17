# This is the dev env specific TF config files.

# Provision the lambda function:
module "lambda" {
  source         = "../../modules/lambda"
  project_prefix = var.project_prefix
  aws_region     = var.aws_region
  source_dir     = "${path.module}/../../../src"
}

# Provision the API Gateway:
module "api_gateway" {
  source              = "../../modules/api_gateway"
  project_prefix      = var.project_prefix
  aws_region          = var.aws_region
  lambda_function_arn = module.lambda.lambda_function_arn
}

# Provision the Cognito User Pool and App Client:
module "cognito" {
  source         = "../../modules/cognito"
  project_prefix = var.project_prefix
  aws_region     = var.aws_region
}