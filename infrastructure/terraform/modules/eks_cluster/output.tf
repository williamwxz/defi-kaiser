output "endpoint" {
  description = "endpoint of cluster"
  value       = aws_eks_cluster.eks_cluster.endpoint
}

output "eks_cluster_name" {
  description = "the name of cluster"
  value       = aws_eks_cluster.eks_cluster.name
}