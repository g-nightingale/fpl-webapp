variable "name" {
    description = "Eventbridge resource name"
    type        = string 
}

variable "schedule_expression" {
  description   = "Cron expression for lambda function"
  type          = string
}
variable "schedule_state" {
  description = "Toggle whether schedule is enabled or not - ENABLED or DISABLED"
  type        = string
}

variable "target_function_arn" {
  description   = "Arn for lambda function"
  type          = string   
}

variable "target_function_name" {
  description   = "Name of target function"
  type          = string   
}

variable "target_function_role_name" {
  description = "Role name of the target function for policy assignment"
  type        = string
}