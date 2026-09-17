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
        Resource = "arn:aws:logs:*:*:log-group:/aws/lambda/${var.project_prefix}-function:*"
      },
      {
        Action = [
          "ec2:CreateVpc",
          "ec2:CreateSubnet",
          "ec2:CreateTags"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action   = ["dynamodb:PutItem"]
        Effect   = "Allow"
        Resource = var.dynamodb_table_arn
      },
    ]
  })
}

# Zip the lambda function code:
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${path.root}/build/lambda.zip"
}

# Lambda function resource:
resource "aws_lambda_function" "lambda_function" {
  function_name = "${var.project_prefix}-function"
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = "app.lambda_handler"
  runtime       = "python3.12"

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = var.dynamodb_table_name
    }
  }

  # Path to the deployment package (ZIP file)
  filename = data.archive_file.lambda_zip.output_path
  # Check the SHA256 for code changes to rebuild the zip:
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}
