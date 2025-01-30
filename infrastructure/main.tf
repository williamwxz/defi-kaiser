# terraform/main.tf
provider "aws" {
  region = "us-east-1"  # Lowest latency for USDC trading
}

# Minimal VPC configuration optimized for high-frequency trading
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "defi-kaiser-vpc"
  cidr = "10.0.0.0/16"

  # Critical for low-latency trading node placement
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  # Essential for blockchain node communication
  enable_nat_gateway = true
  single_nat_gateway = true  # Cost optimization
}

# Optimized EKS cluster configuration
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.15.3"

  cluster_name    = "defi-kaiser"
  cluster_version = "1.27"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Critical node group configuration for trading workloads
  eks_managed_node_groups = {
    trading-nodes = {
      min_size     = 1
      max_size     = 3  # Auto-scale during volatility spikes
      desired_size = 2

      # Optimized instance type balance between memory and CPU
      instance_types = ["m6i.large"]  # 3rd gen Intel Xeon, 8GB RAM

      # Essential trading node requirements
      capacity_type  = "SPOT"      # 60-70% cost savings
      labels = {
        workload-type = "latency-sensitive"
      }

      # Node security configuration
      iam_role_additional_policies = {
        AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
      }
    }
  }

  # Critical security group rules for blockchain access
  cluster_security_group_additional_rules = {
    blockchain_outbound = {
      description      = "Allow all outbound to blockchain nodes"
      protocol         = "-1"
      from_port        = 0
      to_port          = 0
      type             = "egress"
      cidr_blocks      = ["0.0.0.0/0"]
    }
  }
}

# Required Kubernetes provider configuration
provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
  }
}

# Verify cluster access
resource "null_resource" "verify_cluster" {
  provisioner "local-exec" {
    command = <<-EOT
      echo "Testing cluster access..."
      kubectl get nodes --kubeconfig <(aws eks update-kubeconfig --name ${module.eks.cluster_name})
    EOT
  }

  depends_on = [module.eks]
}