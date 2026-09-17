### What does this TF module do ?

- This module provisions AWS DynamoDB Table.

### How to import this child module ?

```bash
# In your parent/caller module, import the module directory as below.

module "dynamodb" {
  source         = "../../modules/dynamodb"
  project_prefix = var.project_prefix
  aws_region     = var.aws_region
}
```