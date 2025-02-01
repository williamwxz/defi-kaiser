
data "aws_availability_zones" "available" {
  provider = aws.primary
}

locals {
  azs = slice(data.aws_availability_zones.available.names, 0, 3)
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${var.prefix}-vpc"
  cidr = var.vpc_cidr

  azs             = slice(data.aws_availability_zones.available.names, 0, 3)
  private_subnets = var.private_subnets_cidr
  public_subnets  = var.public_subnets_cidr

  enable_nat_gateway = true
  enable_vpn_gateway = false

  tags = {
    Terraform = "true"
  }

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.prefix}-eks-cluster" = "shared"
    "kubernetes.io/role/elb"                          = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${var.prefix}-eks-cluster" = "shared"
    "kubernetes.io/role/internal-elb"                 = "1"
  }
}
