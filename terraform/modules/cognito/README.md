### What does this TF module do ?

- This module provisions AWS Cognito with the following resources:
  - AWS Cognito Userpool.
  - AWS Cognito Client App.


### How to import this child module ?

```bash
# In your parent/caller module, import the module directory as below.

# Provision the Cognito User Pool and App Client:
module "cognito" {
  source         = "../../modules/cognito"
  project_prefix = var.project_prefix
  aws_region     = var.aws_region
}
```