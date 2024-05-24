variable "function_name" {
  description   = "Name of the lambda function"
  type          = string 
}

variable "repository_url" {
  description   = "ECR repository URL"
  type          = string 
}

variable "timeout" {
  description   = "Lambda function timeout"
  type          = number   
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

variable "image_tag" {
  description   = "Tag of the docker image"
  type          = string
}

variable "attach_dynamodb_policy" {
  type        = bool
  description = "Whether to attach DynamoDB policy to the Lambda function's role"
  default     = false
}

variable "dynamodb_table_arn" {
  type        = string
  description = "ARN of the DynamoDB table"
  default     = ""
}