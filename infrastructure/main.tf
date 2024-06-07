provider "aws" {
  region  = "eu-west-2"
  profile = "default"
}

module "s3_bucket" {
  source         = "./modules/s3"
  bucket_name    = "gn-s3"
}

module "ecr_repo_lambda_extract" {
  source          = "./modules/ecr"
  repository_name = "lambda-extract"
}

module "ecr_repo_lambda_transform" {
  source          = "./modules/ecr"
  repository_name = "lambda-transform"
}

module "ecr_repo_lambda_points_prediction" {
  source          = "./modules/ecr"
  repository_name = "lambda-points-prediction"
}

module "ecr_repo_lambda_points_pred_dynamo" {
  source          = "./modules/ecr"
  repository_name = "lambda-points-pred-dynamo"
}

module "lambda_function_extract" {
  source             = "./modules/lambda_function_from_image"
  function_name       = "fpl_extract_and_load"
  repository_url      = module.ecr_repo_lambda_extract.ecr_repository_url
  image_tag           = "latest" 
  memory_size         = 512
  timeout             = 600
  secret_arn          = "arn:aws:secretsmanager:eu-west-2:264673220706:secret:rds_secrets-P26F8L"
}

module "lambda_function_transform" {
  source             = "./modules/lambda_function_from_image"
  function_name       = "fpl_transform"
  repository_url      = module.ecr_repo_lambda_transform.ecr_repository_url
  image_tag           = "latest" 
  memory_size         = 1024
  timeout             = 600
  secret_arn          = "arn:aws:secretsmanager:eu-west-2:264673220706:secret:rds_secrets-P26F8L"
}

module "lambda_function_points_prediction" {
  source             = "./modules/lambda_function_from_image"
  function_name       = "fpl_points_prediction"
  repository_url      = module.ecr_repo_lambda_points_prediction.ecr_repository_url
  image_tag           = "latest" 
  memory_size         = 2048
  timeout             = 600
  secret_arn          = "arn:aws:secretsmanager:eu-west-2:264673220706:secret:rds_secrets-P26F8L"
}

module "lambda_function_points_pred_dynamodb" {
  source             = "./modules/lambda_function_from_image"
  function_name       = "fpl_points_pred_dynamodb"
  repository_url        = module.ecr_repo_lambda_points_pred_dynamo.ecr_repository_url
  image_tag              = "latest" 
  memory_size            = 256
  timeout                = 600
  secret_arn             = "arn:aws:secretsmanager:eu-west-2:264673220706:secret:rds_secrets-P26F8L"
  attach_dynamodb_policy = true
  dynamodb_table_arn     = module.dynamodb_player_points.dynamodb_arn
}

module "fpl_step_function" {
  source             = "./modules/step_function"
  step_function_name = "fpl_step_function"
  secret_arn         = "arn:aws:secretsmanager:eu-west-2:264673220706:secret:rds_secrets-P26F8L"
  definition = <<EOF
{
  "Comment": "AWS Step Functions to orchestrate FPL pipelines.",
  "StartAt": "fpl_extract",
  "States": {
    "fpl_extract": {
      "Type": "Task",
      "Resource": "${module.lambda_function_extract.lambda_function_arn}",
      "Next": "fpl_transform"
    },
    "fpl_transform": {
      "Type": "Task",
      "Resource": "${module.lambda_function_transform.lambda_function_arn}",
      "Next": "fpl_points_prediction"
    },
    "fpl_points_prediction": {
    "Type": "Task",
    "Resource": "${module.lambda_function_points_prediction.lambda_function_arn}",
    "Next": "fpl_points_points_pred_dynamodb"
    },
    "fpl_points_points_pred_dynamodb": {
    "Type": "Task",
    "Resource": "${module.lambda_function_points_pred_dynamodb.lambda_function_arn}",
    "End": true
    }
  }
}
EOF
}

module "eventbridge_step_function" {
  source                    = "./modules/eventbridge"
  name                      = "eventbridge_extract"
  schedule_expression       = "cron(0 3 * * ? *)"
  target_function_arn       = module.fpl_step_function.step_function_arn
  target_function_name      = module.fpl_step_function.step_function_name
  target_function_role_name = module.fpl_step_function.step_function_role_name
  schedule_state            = "DISABLED"
}

module "rds_postgres_db" {
  source               = "./modules/rds"
  identifier           = "gn-rds"
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "16.1"
  instance_class       = "db.t3.micro"
  db_name              = "gn_rds"
  publicly_accessible  = true
  username             = "postgres"
  password             = "postgres1234"
  parameter_group_name = "default.postgres16"
  allowed_ips           = ["86.189.206.136/32", "0.0.0.0/0"]
  skip_final_snapshot  = true
}

module "dynamodb_player_points" {
  source          = "./modules/dynamodb"
  name            = "player_points_predictions"
  billing_mode    = "PAY_PER_REQUEST"
  hash_key        = "element"
  tags            = {
    name = "player_predictions"
  }

  attribute_definitions = [
    {
      name = "element"
      type = "N"
    },
    // Add more attributes as needed
  ]
}