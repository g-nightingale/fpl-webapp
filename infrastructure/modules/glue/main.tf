variable "bucket_path" {}
variable "database_name" {}
variable "glue_crawler_name" {}

resource "aws_iam_role" "glue_service_role" {
  name = "AWSGlueServiceRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "glue_service_policy" {
  name        = "GlueServicePolicy"
  path        = "/"
  description = "AWS Glue Service Role Permissions"
  policy      = data.aws_iam_policy_document.glue_service_policy_doc.json
}

data "aws_iam_policy_document" "glue_service_policy_doc" {
  statement {
    actions = [
      "glue:*",
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy_attachment" "glue_s3_access" {
  name       = "glue-s3-read-access"
  roles      = [aws_iam_role.glue_service_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_iam_policy" "glue_cloudwatch_logs" {
  name        = "GlueCloudWatchLogsPolicy"
  description = "Allow Glue to write logs to CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:eu-west-2:264673220706:*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_service_policy_attach" {
  role       = aws_iam_role.glue_service_role.name
  policy_arn = aws_iam_policy.glue_service_policy.arn
}


resource "aws_iam_policy_attachment" "glue_cloudwatch_logs_attachment" {
  name       = "glue-cloudwatch-logs-attachment"
  roles      = [aws_iam_role.glue_service_role.name]
  policy_arn = aws_iam_policy.glue_cloudwatch_logs.arn
}

# Glue Data Catalog Database
resource "aws_glue_catalog_database" "my_database" {
  name = var.database_name
}

# AWS Glue Crawler
resource "aws_glue_crawler" "my_crawler" {
  name          = var.glue_crawler_name
  role          = aws_iam_role.glue_service_role.arn
  database_name = aws_glue_catalog_database.my_database.name

  s3_target {
    path = var.bucket_path
  }

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }
}
