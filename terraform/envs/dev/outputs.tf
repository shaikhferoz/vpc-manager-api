output "lambda_function_name" {
  value = module.lambda.lambda_function_arn
}

output "api_gateway_url" {
  value = module.api_gateway.api_url
}