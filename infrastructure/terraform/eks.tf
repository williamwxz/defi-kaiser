resource "aws_eks_cluster" "defi_kaiser" {
  name     = "defi-kaiser-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids = [aws_subnet.eks_subnet_a.id, aws_subnet.eks_subnet_b.id]
  }
}

resource "aws_eks_node_group" "workers" {
  cluster_name  = aws_eks_cluster.defi_kaiser.name
  node_role_arn = aws_iam_role.eks_node_role.arn
  subnet_ids    = [aws_subnet.eks_subnet_a.id, aws_subnet.eks_subnet_b.id]
  instance_types = [var.eks_instance_type]

  scaling_config {
    desired_size = 1
    min_size     = 1
    max_size     = 1
  }
}