resource "aws_iam_role_policy_attachment" "eks_policy_attachment_1" {
  provider = aws.primary
  depends_on = [
    aws_iam_role.eks_iam_role
  ]

  role       = aws_iam_role.eks_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_iam_role_policy_attachment" "eks_policy_attachment_2" {
  provider = aws.primary
  depends_on = [
    aws_iam_role.eks_iam_role
  ]

  role       = aws_iam_role.eks_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
}

resource "aws_iam_role_policy_attachment" "eks_policy_attachment_3" {
  provider = aws.primary
  depends_on = [
    aws_iam_role.eks_iam_role,
    aws_iam_policy.eks_cluster_policy
  ]

  role       = aws_iam_role.eks_iam_role.name
  policy_arn = aws_iam_policy.eks_cluster_policy.arn
}

resource "aws_iam_role_policy_attachment" "nodegroup_policy_attachment" {
  provider = aws.primary
  depends_on = [
    aws_iam_role.eks_nodegroup_iam_role
  ]
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
    "arn:aws:iam::aws:policy/AmazonEKSServicePolicy",
    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
    "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
    "arn:aws:iam::aws:policy/SecretsManagerReadWrite",
    "arn:aws:iam::aws:policy/AmazonRDSDataFullAccess",
    "arn:aws:iam::aws:policy/AmazonAthenaFullAccess",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
  ])

  role       = aws_iam_role.eks_nodegroup_iam_role.name
  policy_arn = each.value
}

resource "aws_iam_role_policy_attachment" "eks_ingress_policy_attachment" {
  provider = aws.primary
  depends_on = [
    aws_iam_role.eks_ingress_iam_role,
    aws_iam_policy.eks_ingress_policy
  ]

  role       = aws_iam_role.eks_ingress_iam_role.name
  policy_arn = aws_iam_policy.eks_ingress_policy.arn
}

resource "aws_iam_role_policy_attachment" "logging_policy_attachment" {
  provider = aws.primary
  depends_on = [
    aws_iam_role.eks_logging_iam_role
  ]

  role       = aws_iam_role.eks_logging_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_role_policy_attachment" "cluster_autoscaler_policy_attachment" {
  provider = aws.primary
  depends_on = [
    aws_iam_role.eks_cluster_autoscaler_iam_role,
    aws_iam_policy.eks_cluster_autoscaler_policy
  ]

  role       = aws_iam_role.eks_cluster_autoscaler_iam_role.name
  policy_arn = aws_iam_policy.eks_cluster_autoscaler_policy.arn
}

resource "aws_iam_role_policy" "nodegroup_inline_policy" {
  provider = aws.primary
  name     = "${var.prefix}-nodegroup-inline-policy"
  role     = aws_iam_role.eks_nodegroup_iam_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ses:Verify*",
          "ses:Send*",
          "ses:Get*",
          "ses:List*"
        ]
        Resource = "*"
      }
    ]
  })
}
