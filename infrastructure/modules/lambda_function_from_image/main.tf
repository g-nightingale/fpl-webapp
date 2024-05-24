locals {
  execution_role_name = "${var.function_name}_execution_role"
  logging_policy_name = "${var.function_name}_logging"
  secrets_policy_name = "${var.function_name}_secrets_manager_policy"
  rds_policy_name     = "${var.function_name}_rds_execution_policy"
}

resource "aws_lambda_function" "lambda_function" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda_execution_role.arn
  package_type     = "Image"
  image_uri        = "${var.repository_url}:${var.image_tag}"
  timeout          = var.timeout
  memory_size      = var.memory_size
}

resource "aws_iam_role" "lambda_execution_role" {
  name = local.execution_role_name

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


data "aws_iam_policy_document" "lambda_logging" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_policy" "lambda_logging" {
  name   = local.logging_policy_name
  policy = data.aws_iam_policy_document.lambda_logging.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

# Policy to allow Lambda to log to CloudWatch and manage RDS
data "aws_iam_policy_document" "lambda_rds_policy_doc" {
  statement {
    actions   = ["rds-db:connect"]
    resources = ["*"]
    effect    = "Allow"
  }
}

resource "aws_iam_policy" "lambda_rds_policy" {
  name        = local.rds_policy_name
  description = "A policy that allows lambda functions to access RDS."
  policy = data.aws_iam_policy_document.lambda_rds_policy_doc.json
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "lambda_rds" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_rds_policy.arn
}

data "aws_iam_policy_document" "lambda_secrets_manager_policy" {
  statement {
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret"
    ]
    resources = [var.secret_arn]
    effect = "Allow"
  }
}

resource "aws_iam_policy" "lambda_secrets_manager_policy" {
  name        = local.secrets_policy_name
  description = "IAM policy for Lambda to access Secrets Manager"
  policy      = data.aws_iam_policy_document.lambda_secrets_manager_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_secrets_manager_attach" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_secrets_manager_policy.arn
}

# IAM Policy for DynamoDB
resource "aws_iam_policy" "lambda_dynamodb_policy" {
  count = var.attach_dynamodb_policy ? 1 : 0 # Create this resource only if attach_dynamodb_policy is true

  name   = "lambda_dynamodb_policy"
  policy = data.aws_iam_policy_document.dynamodb_policy.json
}

data "aws_iam_policy_document" "dynamodb_policy" {
  statement {
    actions   = ["dynamodb:PutItem"]
    resources = [var.dynamodb_table_arn]
    effect    = "Allow"
  }
}

# Attach policy to IAM role
resource "aws_iam_role_policy_attachment" "lambda_dynamodb_attachment" {
  count      = var.attach_dynamodb_policy ? 1 : 0 # Create this resource only if attach_dynamodb_policy is true

  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_dynamodb_policy[0].arn
}
