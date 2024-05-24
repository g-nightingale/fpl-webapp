output "object_key" {
  value       = aws_s3_object.lambda_layer_object.key
  description = "The key of the s3 bucket object"
}

output "object_version_id" {
  value       = aws_s3_object.lambda_layer_object.version_id
  description = "The version of the s3 bucket object"
}
