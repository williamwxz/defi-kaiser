variable "lambda_arn" {
  description = "要触发的Lambda ARN"
  type        = string
}

variable "schedule" {
  description = "定时规则表达式（如 rate(5 minutes)）"
  type        = string
}

variable "rule_name" {
  description = "EventBridge规则名称"
  type        = string
  default     = "lambda-trigger-rule"
}