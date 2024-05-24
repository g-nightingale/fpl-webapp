output "db_name" {
  value = aws_db_instance.rds_db.db_name
  description = "RDS database name."
}

output "db_username" {
  value = aws_db_instance.rds_db.username
  description = "RDS database user name."
}

output "db_password" {
  value = aws_db_instance.rds_db.password
  description = "RDS database user password."
}

output "db_address" {
  value = aws_db_instance.rds_db.address
  description = "RDS database address."
}

output "db_port" {
  value = aws_db_instance.rds_db.port
  description = "RDS database port."
}

output "db_instance_endpoint" {
  value = aws_db_instance.rds_db.endpoint
}

output "db_instance_username" {
  value = aws_db_instance.rds_db.username
}