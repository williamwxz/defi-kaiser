terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = ">=4.36.0"
      configuration_aliases = [aws.primary]
    }
  }
}