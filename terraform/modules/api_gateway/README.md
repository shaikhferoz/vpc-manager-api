### What does this TF module do ?

- This module provisions AWS API Gateway components with the following resources:
  - AWS HTTP API Gateway.
  - AWS API Stage.
  - AWS API Route.
  - AWS Lambda Integration(expects lambda to be already created).
  - AWS lambda resource policy to allow API Gateway to invoke lambda function.

- Dependency as inputs:
  - AWS Lambda function ARN(Created as part of Lambda module)
  - AWS Cognito App Client ID(Created as part of cognito module).
  - AWS Cognito OIDC Issuer URL(Created as part of cognito module).


### How to import this child module ?

```bash
# In your parent/caller module, import the module directory as below.

module "api_gateway" {
  source                = "../../modules/api_gateway"
  project_prefix        = var.project_prefix
  aws_region            = var.aws_region
  lambda_function_arn   = module.lambda.lambda_function_arn
  cognito_app_client_id = module.cognito.app_client_id
  cognito_issuer_url    = module.cognito.issuer_url
}
```