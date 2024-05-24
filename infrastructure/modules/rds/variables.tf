variable "identifier" {
  description = "Database identifier"
  type        = string
}

variable "allocated_storage" {
  description = "Database storage"
  type        = number
  default     = 20
}

variable "engine" {
  description = "Database storage"
  type        = string
}

variable "engine_version" {
  description = "Database engine version"
  type        = string
}

variable "instance_class" {
  description = "Database instance class"
  type        = string
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "publicly_accessible" {
  description = "Whether database is publicly accessible or not"
  type        = bool
}

variable "username" {
  description = "Database username"
  type        = string
}

variable "password" {
  description = "Database password"
  type        = string
}

variable "parameter_group_name" {
  description = "Parameter group name"
  type        = string
}

variable "skip_final_snapshot" {
  description = "Whether to skip final snapshot"
  type        = bool
}

variable "allowed_ips" {
  description = "IP address to allow access to the RDS instance"
  type        = list(string)
  default     = []  # Default to an empty list if no IPs are specified
}
