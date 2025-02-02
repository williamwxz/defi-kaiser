resource "aws_iam_role" "eks_iam_role" {
  provider = aws.primary

  name               = "${var.prefix}_eks_iam_role"
  path               = "/"
  assume_role_policy = var.eks_assume_role_policy_file

  tags = {
    managed_by = "terraform"
  }
}

resource "aws_iam_role" "eks_nodegroup_iam_role" {
  provider = aws.primary

  name               = "${var.prefix}_nodegroup_iam_role"
  path               = "/"
  assume_role_policy = var.eks_nodegroup_assume_role_policy_file

  tags = {
    managed_by = "terraform"
  }
}

resource "aws_iam_role" "eks_ingress_iam_role" {
  provider = aws.primary

  name = "${var.prefix}_ingress_iam_role"
  path = "/"
  assume_role_policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Effect : "Allow",
        Principal : {
          "Federated" : "arn:aws:iam::${var.account_id}:oidc-provider/${replace(aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer, "https://", "")}"
        },
        Action : "sts:AssumeRoleWithWebIdentity",
        Condition : {
          StringEquals : {
            "${replace(aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer, "https://", "")}:aud" : "sts.amazonaws.com",
            "${replace(aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer, "https://", "")}:sub" : "system:serviceaccount:kube-system:aws-load-balancer-controller-1"
          }
        }
      }
    ]
  })

  tags = {
    managed_by = "terraform"
  }
}

resource "aws_iam_role" "eks_logging_iam_role" {
  provider = aws.primary

  name = "${var.prefix}_eks_logging_iam_role"
  path = "/"
  assume_role_policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Effect : "Allow",
        Principal : {
          "Federated" : "arn:aws:iam::${var.account_id}:oidc-provider/${replace(aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer, "https://", "")}"
        },
        Action : "sts:AssumeRoleWithWebIdentity",
        Condition : {
          StringEquals : {
            "${replace(aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer, "https://", "")}:sub" : "system:serviceaccount:production:logging-sa",
            "${replace(aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer, "https://", "")}:aud" : "sts.amazonaws.com"
          }
        }
      }
    ]
  })

  tags = {
    managed_by = "terraform"
  }
}

resource "aws_iam_role" "eks_cluster_autoscaler_iam_role" {
  provider = aws.primary

  name = "${var.prefix}_eks_cluster_autoscaler_iam_role"
  path = "/"
  assume_role_policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Effect : "Allow",
        Principal : {
          "Federated" : "arn:aws:iam::${var.account_id}:oidc-provider/${replace(aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer, "https://", "")}}"
        },
        Action : "sts:AssumeRoleWithWebIdentity",
        Condition : {
          StringEquals : {
            "${replace(aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer, "https://", "")}:sub" : "system:serviceaccount:kube-system:cluster-autoscaler",
            "${replace(aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer, "https://", "")}:aud" : "sts.amazonaws.com"
          }
        }
      }
    ]
  })

  tags = {
    managed_by = "terraform"
  }
}

resource "aws_iam_openid_connect_provider" "cluster_openid_provider" {
  url             = aws_eks_cluster.eks_cluster.identity[0].oidc[0].issuer
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = var.thumbprint_list

  depends_on = [aws_eks_cluster.eks_cluster]
}
