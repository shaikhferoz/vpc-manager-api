output "lambda_function_name" {
  value = module.lambda.lambda_function_arn
}

output "api_gateway_url" {
  value = module.api_gateway.api_url
}

output "cognito_user_pool_id" {
  value = module.cognito.user_pool_id
}

output "cognito_app_client_id" {
  value = module.cognito.app_client_id
}