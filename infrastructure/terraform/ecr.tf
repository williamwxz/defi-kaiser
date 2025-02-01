resource "aws_ecr_repository" "defi_kaiser" {
  name                 = "defi-kaiser"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_lifecycle_policy" "defi_kaiser_policy" {
  repository = aws_ecr_repository.defi_kaiser.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1,
      description  = "Expire untagged images after 14 days",
      selection    = {
        tagStatus   = "untagged"
        countType   = "sinceImagePushed"
        countUnit   = "days"
        countNumber = 14
      },
      action       = {
        type = "expire"
      }
    }]
  })
}