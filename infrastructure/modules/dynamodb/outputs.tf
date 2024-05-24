output "dynamodb_arn" {
  description = "The ARN of the dynamodb"
  value       = aws_dynamodb_table.dynamodb_table.arn
}