variable "table_name" {
  description = "DynamoDB表名"
  type        = string
}

variable "hash_key" {
  description = "主键字段名"
  type        = string
  default     = "timestamp"
}

variable "range_key" {
  description = "排序键字段名"
  type        = string
  default     = "protocol"
}