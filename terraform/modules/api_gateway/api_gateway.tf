# The API Gateway HTTP API.
# TBD: No authorizers yet, will add later.
resource "aws_apigatewayv2_api" "api" {
  name          = "${var.project_prefix}-api"
  protocol_type = "HTTP"
}
