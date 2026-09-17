# This is the dev env specific TF config files.

# Provision the lambda function:
module "lambda" {
  source              = "../../modules/lambda"
  project_prefix      = var.project_prefix
  aws_region          = var.aws_region
  source_dir          = "${path.module}/../../../src"
  dynamodb_table_name = module.dynamodb.table_name
  dynamodb_table_arn  = module.dynamodb.table_arn
}

# Provision the API Gateway:
module "api_gateway" {
  source                = "../../modules/api_gateway"
  project_prefix        = var.project_prefix
  aws_region            = var.aws_region
  lambda_function_arn   = module.lambda.lambda_function_arn
  cognito_app_client_id = module.cognito.app_client_id
  cognito_issuer_url    = module.cognito.issuer_url
}

# Provision the Cognito User Pool and App Client:
module "cognito" {
  source         = "../../modules/cognito"
  project_prefix = var.project_prefix
  aws_region     = var.aws_region
}

# Provision AWS DynamoDB table for storing VPC information:
module "dynamodb" {
  source         = "../../modules/dynamodb"
  project_prefix = var.project_prefix
  aws_region     = var.aws_region
}