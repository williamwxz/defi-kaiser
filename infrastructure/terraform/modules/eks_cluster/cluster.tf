resource "aws_eks_cluster" "eks_cluster" {
  provider = aws.primary
  depends_on = [
    aws_iam_role_policy_attachment.eks_policy_attachment_1,
    aws_iam_role_policy_attachment.eks_policy_attachment_2,
    aws_iam_role_policy_attachment.eks_policy_attachment_3
  ]

  name     = "${var.prefix}-eks-cluster"
  role_arn = aws_iam_role.eks_iam_role.arn
  version  = var.eks_version

  vpc_config {
    subnet_ids = concat(
      sort(var.public_subnet_ids),
      sort(var.private_subnet_ids)
    )
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = var.eks_whitelisted_ips

  }

  tags = {
    managed_by = "terraform"
  }
}