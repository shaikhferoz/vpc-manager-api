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

# IAM policy with required permissions for the lambda:
resource "aws_iam_role_policy" "lambda_iam_policy" {
  name = "${var.project_prefix}-lambda-iam-policy"
  role = aws_iam_role.lambda_execution_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      },
    ]
  })
}