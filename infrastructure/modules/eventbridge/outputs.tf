output "rule_arn" {
  description = "EventBridge规则ARN"
  value       = aws_cloudwatch_event_rule.this.arn
}