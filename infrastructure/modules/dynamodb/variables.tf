variable "name" {
  description = "Dynamodb table name"
  type        = string
  default     = "dynamo_db_table"
}

variable "billing_mode" {
  description = "Billing mode"
  type        = string
  default     = "PAY_PER_REQUEST"
}

variable "hash_key" {
  description = "Hash key for table"
  type        = string    
}

variable "attribute_definitions" {
  description = "A list of attribute definitions"
  type = list(object({
    name = string
    type = string
  }))
}

variable "tags" {
    description = "A map of tags to add to all resources"
    type        = map(string)
    default     = {
    Environment = "Development"
  }
}
