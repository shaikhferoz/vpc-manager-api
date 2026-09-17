# This is the dev env specific TF config files.
module "lambda" {
  source         = "../../modules/lambda"
  project_prefix = var.project_prefix
  aws_region     = var.aws_region
}