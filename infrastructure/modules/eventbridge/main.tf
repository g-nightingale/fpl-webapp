locals {
  schedule_name         = "${var.name}_schedule"
  eventbridge_role_name = "${var.name}_step_function_role"
  execution_policy_name = "${var.name}_logging"
  target_id             = "${var.target_function_name}_target"
}

resource "aws_cloudwatch_event_rule" "schedule_rule" {
  name                = local.schedule_name
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "service_target" {
  rule      = aws_cloudwatch_event_rule.schedule_rule.name
  target_id = local.target_id
  arn       = var.target_function_arn
  role_arn  = aws_iam_role.eventbridge_sfn_role.arn
}

# resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
#   statement_id  = "AllowExecutionFromCloudWatch"
#   action        = "lambda:InvokeFunction"
#   function_name = var.target_function_name
#   principal     = "events.amazonaws.com"
#   source_arn    = aws_cloudwatch_event_rule.schedule_rule.arn
# }

resource "aws_iam_role" "eventbridge_sfn_role" {
  name = local.eventbridge_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "events.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "eventbridge_sfn_policy" {
  name        = local.execution_policy_name
  description = "Allows EventBridge to execute a specific Step Function"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "states:StartExecution"
        Resource = "${var.target_function_arn}"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eventbridge_sfn_policy_attachment" {
  role       = aws_iam_role.eventbridge_sfn_role.name
  policy_arn = aws_iam_policy.eventbridge_sfn_policy.arn
}

