resource "aws_dynamodb_table" "this" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "timestamp"
  range_key    = "protocol"

  attribute {
    name = "timestamp"
    type = "N"
  }

  attribute {
    name = "protocol"
    type = "S"
  }
}