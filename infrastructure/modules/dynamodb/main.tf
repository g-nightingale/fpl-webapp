resource "aws_dynamodb_table" "dynamodb_table" {
  name           = var.name
  billing_mode   = var.billing_mode
  hash_key       = var.hash_key

  dynamic "attribute" {
    for_each = var.attribute_definitions
    content {
      name = attribute.value.name
      type = attribute.value.type
    }
  }

  tags = var.tags
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

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

resource "aws_iam_policy" "lambda_dynamodb_rds_policy" {
  name        = "lambda_dynamodb_rds_policy"
  description = "IAM policy for accessing RDS and DynamoDB from Lambda"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "rds-db:connect",
          "dynamodb:PutItem",
          "dynamodb:BatchWriteItem",
          // Add more DynamoDB permissions as needed
        ]
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_rds_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_dynamodb_rds_policy.arn
}
