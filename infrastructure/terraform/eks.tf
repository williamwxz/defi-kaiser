resource "aws_eks_cluster" "defi_kaiser" {
  name     = "defi-kaiser-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn

  depends_on = [
    aws_iam_role.eks_cluster_role
  ]

  vpc_config {
    subnet_ids = module.vpc.private_subnets
  }
}

resource "aws_eks_node_group" "workers" {
  cluster_name   = aws_eks_cluster.defi_kaiser.name
  node_group_name = "defi_kaiser_workers"
  node_role_arn  = aws_iam_role.eks_node_role.arn
  # subnet_ids     = [aws_subnet.eks_subnet_a.id, aws_subnet.eks_subnet_b.id]
  subnet_ids      = module.vpc.private_subnets
  instance_types = [var.eks_instance_type]
  capacity_type  = "ON_DEMAND"
  ami_type       = "AL2_x86_64"
  disk_size      = 20

  depends_on = [
    aws_eks_cluster.defi_kaiser,
    aws_iam_role.eks_node_role
  ]

  scaling_config {
    desired_size = 1
    min_size     = 1
    max_size     = 1
  }

  tags = {
    "eks:cluster-name" = aws_eks_cluster.defi_kaiser.name
  }
}
