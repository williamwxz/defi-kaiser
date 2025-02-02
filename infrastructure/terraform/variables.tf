############################### Common Variables ###########################
variable "account_id" {
  description = "aws account id"
  default     = "598670062096"
}

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

################################# EKS Variables ###########################


variable "eks_version" {
  type        = string
  description = "Control plane version for the kubernetes cluster"
  default     = "1.32"
}

variable "eks_whitelisted_ips" {
  type        = list(string)
  description = "List of IP addresses which can access Kubernetes cluster publicly"
  default     = ["0.0.0.0/0"]
}

variable "nodegroup_ami_type" {
  type        = string
  description = "AMI type of the instances for primary node group"
  default     = "AL2_x86_64"
}

variable "nodegroup_capacity_type" {
  type        = string
  description = "Instance capacity type for primary node group"
  default     = "ON_DEMAND"
}

variable "nodegroup_disk_size" {
  type        = string
  description = "Disk size attached to the primary instances"
  default     = "20"
}

variable "nodegroup_instance_type" {
  type        = list(string)
  description = "Instance types for the primary node group"
  default     = ["t3.micro"]
}

variable "nodegroup_desired_size" {
  type        = number
  description = "desired size of the primary node group"
  default     = 1
}

variable "nodegroup_max_size" {
  type        = number
  description = "maximum number of instances in primary node group"
  default     = 2
}

variable "nodegroup_min_size" {
  type        = number
  description = "minimum number of instance in primary node group"
  default     = 1
}

variable "nodegroup_max_unavailable" {
  type        = number
  description = "maximum number of unavailable instance in the node group"
  default     = 1
}