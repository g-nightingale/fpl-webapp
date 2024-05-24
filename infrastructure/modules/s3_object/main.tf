resource "aws_s3_object" "lambda_layer_object" {
  bucket = var.bucket_name
  key    = var.s3_key
  source = var.s3_source
  etag   = filemd5(var.s3_source)
}