terraform {
  backend "s3" {
    bucket         = "terraform-state-defi-kaiser"
    key            = "terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
  }
}