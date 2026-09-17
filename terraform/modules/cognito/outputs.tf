output "user_pool_id" {
  value       = aws_cognito_user_pool.user_pool.id
  description = "The ID of the Cognito User Pool."
}

output "app_client_id" {
  value       = aws_cognito_user_pool_client.app_client.id
  description = "The ID of the Cognito App Client."
}

output "issuer_url" {
  value       = "https://cognito-idp.${var.aws_region}.amazonaws.com/${aws_cognito_user_pool.user_pool.id}"
  description = "The OIDC issuer URL used by API Gateway authorizer for JWT validation."
}