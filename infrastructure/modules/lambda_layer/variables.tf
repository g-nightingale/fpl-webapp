variable "layer_name" {
  description = "Lambda layer name"
  type        = string
  default     = "lambda_layer"
}

# variable "filename" {
#   description = "The zip file to be used for the lambda layer"
#   type        = string
#   default     = ""
# }

variable "source_code_hash" {
  description   = "Hash of the source code"
  type          = string 
  default       = ""
}

variable "compatible_runtimes" {
  description = "Compatible runtimes"
  type        = list(string)
  default     = ["python3.9"]
}

variable "description" {
  description = "A description for the lambda layer"
  type        = string
}

variable "s3_bucket" {
  description = "S3 bucket"
  type        = string
  default     = ""
}

variable "s3_key" {
  description = "S3 key"
  type        = string
  default     = ""
}

variable "s3_object_version" {
  description = "s3 object version"
  type        = string
  default     = ""
}

variable "license_info" {
  description = "License information"
  type        = string
  default     = "MIT"
}