resource "aws_eks_addon" "cni" {
  depends_on   = [aws_eks_node_group.eks_nodegroup]
  cluster_name = aws_eks_cluster.eks_cluster.name
  addon_name   = "vpc-cni"
}

resource "aws_eks_addon" "coredns" {
  depends_on   = [aws_eks_node_group.eks_nodegroup]
  cluster_name = aws_eks_cluster.eks_cluster.name
  addon_name   = "coredns"
}

resource "aws_eks_addon" "kubeproxy" {
  depends_on   = [aws_eks_node_group.eks_nodegroup]
  cluster_name = aws_eks_cluster.eks_cluster.name
  addon_name   = "kube-proxy"
}

resource "aws_eks_addon" "ebs" {
  depends_on   = [aws_eks_node_group.eks_nodegroup]
  cluster_name = aws_eks_cluster.eks_cluster.name
  addon_name   = "aws-ebs-csi-driver"
}
