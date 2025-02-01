# eks instance type
variable "eks_instance_type" {
  type    = string
  default = "t3.small"
}

variable "region" {
  description = "enter region"
  default     = "us-west-2"
}

variable "prefix" {
  description = "Prefix for resources"
  default     = "defi-kaiser"
}

variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR block"
  default     = "172.31.0.0/16"
}

variable "public_subnets_cidr" {
  type        = list(string)
  description = "Public Subnet CIDR values"
  default     = ["172.31.0.0/20", "172.31.32.0/20"]
}

variable "private_subnets_cidr" {
  type        = list(string)
  description = "Private Subnet CIDR values"
  default     = ["172.31.48.0/20", "172.31.16.0/20"]
}