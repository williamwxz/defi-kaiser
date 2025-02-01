resource "aws_s3_bucket" "terraform_state" {
  bucket = "defi-kaiser-terraform-state"
  force_destroy = true # WARNING: Only for testing, remove in production
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}