variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "infura_key" {
  description = "Infura API key"
  sensitive   = true
}

variable "private_key" {
  description = "Ethereum wallet private key"
  sensitive   = true
}

variable "lambda_s3_bucket" {
  description = "Lambda代码包存储的S3桶名"
  type        = string
  default     = "defi-kaiser-bot-lambda-code"
}