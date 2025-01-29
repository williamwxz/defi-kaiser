provider "aws" {
  region = var.aws_region
}

module "dynamodb" {
  source     = "./modules/dynamodb"
  table_name = "RWA_Market_Data"
}

module "data_monitor_lambda" {
  source               = "./modules/lambda"
  function_name        = "data-monitor"
  s3_bucket            = var.lambda_s3_bucket
  s3_key               = "data_monitor.zip"
  handler              = "main.lambda_handler"
  runtime              = "python3.8"
  environment_variables = {
    DYNAMODB_TABLE = module.dynamodb.table_name
  }
}

module "trade_executor_lambda" {
  source               = "./modules/lambda"
  function_name        = "trade-executor"
  s3_bucket            = var.lambda_s3_bucket
  s3_key               = "trade_executor.zip"
  handler              = "index.handler"
  runtime              = "nodejs18.x"
  environment_variables = {
    INFURA_KEY  = var.infura_key
    PRIVATE_KEY = var.private_key
  }
}

module "eventbridge" {
  source     = "./modules/eventbridge"
  lambda_arn = module.data_monitor_lambda.arn
  schedule   = "rate(5 minutes)"
}