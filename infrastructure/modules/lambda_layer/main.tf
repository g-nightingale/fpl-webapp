
resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name       = var.layer_name
  # filename         = var.filename  # Path to your layer ZIP file
  # source_code_hash = var.source_code_hash

  s3_bucket         = var.s3_bucket
  s3_key            = var.s3_key
  s3_object_version = var.s3_object_version

  compatible_runtimes = var.compatible_runtimes  # Specify compatible runtime

  # Optional: Add description
  description = var.description

  # Optional: Set license info
  license_info = var.license_info
}
