############################### EKS Module ##########################

module "eks" {
  source     = "./modules/eks_cluster"
  depends_on = [module.vpc]
  providers = {
    aws.primary = aws.primary
  }
  prefix                                   = var.prefix
  account_id                               = var.account_id
  region                                   = var.region
  eks_cluster_policy_file                  = data.local_file.eks_cluster_policy_file.content
  eks_ingress_policy_file                  = data.local_file.eks_ingress_policy_file.content
  cluster_autoscaler_policy_file           = data.local_file.cluster_autoscaler_policy_file.content
  eks_assume_role_policy_file              = data.local_file.eks_assume_role_policy_file.content
  eks_nodegroup_assume_role_policy_file    = data.local_file.eks_nodegroup_assume_role_policy_file.content
  aws_load_balancer_controller_policy_file = data.local_file.aws_load_balancer_controller_policy_file.content
  eks_version                              = var.eks_version
  eks_whitelisted_ips                      = var.eks_whitelisted_ips
  nodegroup_ami_type                       = var.nodegroup_ami_type
  nodegroup_capacity_type                  = var.nodegroup_capacity_type
  nodegroup_desired_size                   = var.nodegroup_desired_size
  nodegroup_disk_size                      = var.nodegroup_disk_size
  nodegroup_instance_type                  = var.nodegroup_instance_type
  nodegroup_max_size                       = var.nodegroup_max_size
  nodegroup_min_size                       = var.nodegroup_min_size
  nodegroup_max_unavailable                = var.nodegroup_max_unavailable
  public_subnet_ids                        = module.vpc.public_subnets
  private_subnet_ids                       = module.vpc.private_subnets
}
