### What does this TF module do ?

- This module provisions AWS lambda function with the following resources:
  - AWS lambda function.
  - AWS lambda IAM execution role.
  - AWS IAM policy.


### How to import this child module ?

```bash
# In your parent/caller module, import the module directory as below.

module "lambda" {
  source = "../../modules/lambda"
  project_prefix = var.project_prefix
  aws_region = var.aws_region
}
```