output "arn" {
  description = "Lambda函数的ARN"
  value       = aws_lambda_function.this.arn
}

output "function_name" {
  description = "Lambda函数名称"
  value       = aws_lambda_function.this.function_name
}