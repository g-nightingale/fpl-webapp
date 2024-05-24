variable "function_name" {
  description   = "Name of the lambda function"
  type          = string 
}

variable "filename" {
  description   = "Path to the zip file for the lambda function"
  type          = string 
}

variable "handler" {
  description   = "Lambda function handler"
  type          = string 
}

variable "runtime" {
  description   = "Lambda function runtime"
  type          = string 
  default       = "python3.9"
}

variable "source_code_hash" {
  description   = "Hash of the source code"
  type          = string 
}

variable "timeout" {
  description   = "Lambda function timeout"
  type          = number   
}

variable "bucket_name" {
  description   = "S3 bucket name"
  type          = string   
}

variable "enable_s3_access" {
  description = "Whether to create IAM policy for S3 access"
  type        = bool
  default     = false
}

variable "lambda_layers" {
  description = "A list of Lambda layer ARNs to be used with Lambda functions"
  type        = list(string)
  default     = []
}

variable "secret_arn" {
  description   = "Arn of secret"
  type          = string
}

variable "memory_size" {
  description   = "Memory for lambda function"
  type          = number
  default       = 128
}