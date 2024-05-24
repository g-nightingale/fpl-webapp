output "lambda_layer_arn" {
  description = "The ARN of the Lambda layer"
  value       = aws_lambda_layer_version.lambda_layer.arn
}