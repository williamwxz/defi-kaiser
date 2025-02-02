resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

resource "aws_iam_role" "github_oidc_role" {
  name = "GitHubAction-AssumeRoleWithAction"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringLike = {
            "token.actions.githubusercontent.com:sub" : "repo:williamwxz/defi-kaiser",
            "token.actions.githubusercontent.com:aud" : "sts.amazonaws.com"
          }
        }
      }
    ]
  })
}

resource "aws_iam_policy" "custom_policy" {
  name        = "github-action-custom-policy"
  description = "Custom policy for github action role"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "ec2:DescribeInstances"
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "eks:ListNodegroups",
          "eks:DescribeFargateProfile",
          "eks:ListTagsForResource",
          "eks:ListAddons",
          "eks:DescribeAddon",
          "eks:ListFargateProfiles",
          "eks:DescribeNodegroup",
          "eks:ListUpdates",
          "eks:DescribeUpdate",
          "eks:AccessKubernetesApi",
          "eks:DescribeCluster",
          "eks:ListClusters",
          "eks:DescribeAddonVersions",
          "eks:UpdateNodegroupConfig",
          "secretsmanager:*",
          "logs:*",
          "acm:*",
          "route53:List*",
          "route53:Get*",
          "ssm:Get*",
          "cloudformation:*",
          "glue:*",
          "ssm:*",
          "sso:*",
          "cloudfront:*",
          "dynamodb:*",
          "bedrock:*",
          "textract:*",
          "sagemaker:*",
          "aws-marketplace:ViewSubscriptions",
          "aws-marketplace:Subscribe",
          "lambda:ListFunctions",
          "aoss:*",
          "textract:AnalyzeDocument",
          "comprehend:DetectDominantLanguage",
          "comprehend:DetectEntities",
          "comprehend:DetectPiiEntities",
          "comprehend:DetectKeyPhrases",
          "comprehend:ClassifyDocument",
        ],
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "custom_role_policy_attachment" {
  role       = aws_iam_role.github_oidc_role.name
  policy_arn = aws_iam_policy.custom_policy.arn
  depends_on = [aws_iam_policy.custom_policy]
}

resource "aws_iam_role_policy_attachment" "github_oidc_role_policy" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
    "arn:aws:iam::aws:policy/AmazonRDSFullAccess",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/IAMFullAccess",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess",
    "arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator",
    "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy",
    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
    "arn:aws:iam::aws:policy/AmazonSESFullAccess",
  ])

  role       = aws_iam_role.github_oidc_role.name
  policy_arn = each.value
}
