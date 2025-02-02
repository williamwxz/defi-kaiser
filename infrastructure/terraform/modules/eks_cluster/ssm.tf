resource "aws_ssm_parameter" "alchemy_webhook_ids" {
  name  = "/project-lighthouse/alchemy/loanfactory/webhookIds"
  type  = "StringList"
  value = "placeholder"

  tags = {
    managed_by = "terraform"
  }
}
