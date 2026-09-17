# Lambda execution role:
# This is the execution role that Lambda service assumes when it runs this function.
resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.project_prefix}-lambda-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}
