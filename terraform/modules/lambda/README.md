### How to import this child module

```bash
# In your parent/caller module, import the current directory as below.

module "lambda" {
  source = "../../modules/lambda"
  project_prefix = var.project_prefix
  aws_region = var.aws_region
}
```