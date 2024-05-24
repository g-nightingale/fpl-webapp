variable "bucket_name" {
    description     = "Name of the S3 bucket"
    type            = string
}

variable "s3_key" {
    description     = "S3 object key"
    type            = string
    default         = ""   
}

variable "s3_source" {
    description     = "S3 object local source"
    type            = string
    default         = ""
}