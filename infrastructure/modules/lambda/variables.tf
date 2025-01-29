variable "function_name" {
  description = "Lambda函数名称"
  type        = string
}

variable "s3_bucket" {
  description = "Lambda代码包存储的S3桶名"
  type        = string
}

variable "s3_key" {
  description = "S3中代码包的路径"
  type        = string
}

variable "handler" {
  description = "Lambda处理函数入口"
  type        = string
}

variable "runtime" {
  description = "Lambda运行时环境"
  type        = string
  default     = "python3.8"
}

variable "environment_variables" {
  description = "Lambda环境变量"
  type        = map(string)
  default     = {}
}