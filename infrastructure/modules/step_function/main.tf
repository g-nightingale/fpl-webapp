locals {
  execution_role_name = "${var.step_function_name}_step_function_execution_role"
  secrets_policy_name = "${var.step_function_name}_secrets_manager_policy"
  rds_policy_name     = "${var.step_function_name}_rds_execution_policy"
}

resource "aws_sfn_state_machine" "sfn_state_machine" {
  name          = var.step_function_name
  role_arn      = aws_iam_role.step_functions_iam_role.arn
  definition    = var.definition
}

resource "aws_iam_role" "step_functions_iam_role" {
  name = local.execution_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "states.amazonaws.com"
        }
        Effect = "Allow"
        Sid    = ""
      },
    ]
  })
}

resource "aws_iam_policy" "invoke_all_lambdas_policy" {
  name        = "${local.execution_role_name}_invoke_all_lambdas_policy"
  description = "Allows invocation of all Lambda functions in the account"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "lambda:InvokeFunction",
        Resource = "arn:aws:lambda:*:*:function:*"
      }
    ]
  })
}


resource "aws_iam_policy_attachment" "attach_invoke_all_lambdas" {
  name       = "${local.execution_role_name}_invoke_all_lambdas_attachment"
  roles      = [aws_iam_role.step_functions_iam_role.name]
  policy_arn = aws_iam_policy.invoke_all_lambdas_policy.arn
}

# Policy to allow Lambda to log to CloudWatch and manage RDS
data "aws_iam_policy_document" "rds_policy_doc" {
  statement {
    actions   = ["rds-db:connect"]
    resources = ["*"]
    effect    = "Allow"
  }
}

resource "aws_iam_policy" "rds_policy" {
  name        = local.rds_policy_name
  description = "A policy that allows step functions to access RDS."
  policy      = data.aws_iam_policy_document.rds_policy_doc.json
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "lambda_rds" {
  role       = aws_iam_role.step_functions_iam_role.name
  policy_arn = aws_iam_policy.rds_policy.arn
}

data "aws_iam_policy_document" "step_function_secrets_manager_policy" {
  statement {
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret"
    ]
    resources = [var.secret_arn]
    effect = "Allow"
  }
}

resource "aws_iam_policy" "step_function_secrets_manager_policy" {
  name        = local.secrets_policy_name
  description = "IAM policy for Step Function to access Secrets Manager"
  policy      = data.aws_iam_policy_document.step_function_secrets_manager_policy.json
}

resource "aws_iam_role_policy_attachment" "step_function_secrets_manager_attach" {
  role       = aws_iam_role.step_functions_iam_role.name
  policy_arn = aws_iam_policy.step_function_secrets_manager_policy.arn
}