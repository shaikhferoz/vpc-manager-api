# The authentication layer to our API is provided by Cognito.

# User pool holds the user accounts and their attributes:
resource "aws_cognito_user_pool" "user_pool" {
  name = "${var.project_prefix}-user-pool"
}

# App Client is the application that will be using the user pool for authentication:
resource "aws_cognito_user_pool_client" "app_client" {
  name         = "${var.project_prefix}-app-client"
  user_pool_id = aws_cognito_user_pool.user_pool.id

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH", # Allows the user to sign in with a username and password.
    "ALLOW_REFRESH_TOKEN_AUTH"  # Allows the user to refresh their access token using a refresh token.
  ]
}