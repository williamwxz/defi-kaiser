output "table_name" {
  description = "DynamoDB表名"
  value       = aws_dynamodb_table.this.name
}

output "table_arn" {
  description = "DynamoDB ARN"
  value       = aws_dynamodb_table.this.arn
}