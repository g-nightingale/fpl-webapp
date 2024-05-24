output "step_function_arn" {
  description = "The ARN of the step function"
  value       = aws_sfn_state_machine.sfn_state_machine.arn
}

output "step_function_name" {
  description = "The name of the step function"
  value       = aws_sfn_state_machine.sfn_state_machine.name
}

output "step_function_role_name" {
  description = "Role name of the step function"
  value       = aws_iam_role.step_functions_iam_role.name
}