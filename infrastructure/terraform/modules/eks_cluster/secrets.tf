resource "aws_secretsmanager_secret" "infura_api_key" {
    name = "infura-api-key"

    tags = {
      managed_by = "terraform"
      team       = "developer"
    }
}