# terraform/variables.tf
variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "defi-kaiser"  # Keep this short for AWS resource naming
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"    # Optimal for USDC trading liquidity
}

variable "trading_node_instance_type" {
  description = "Instance type for trading nodes"
  type        = string
  default     = "m6i.large"    # Balance of compute/memory for quant workloads
}