### This directory represents a DEV AWS account/environment

- Here, the parent directory structure `dev` represents the `dev` environment.
- Ensure you have configured the required AWS_profile that is able to talk to AWS APIs from wherever you are running the TF plan/apply.
- Since this is the `root` module calling the lambda `child` module, all TF commands shall be executed from this directory.


### Provisioning the remote backend(1st time)

```bash
export AWS_PROFILE=admin_awslabs
export AWS_REGION=us-east-1
export TF_STATE_BUCKET=awslabs-terraform-state-433306737932

aws sts get-caller-identity --profile "$AWS_PROFILE"

aws s3api create-bucket \
  --bucket "$TF_STATE_BUCKET" \
  --region "$AWS_REGION"

aws s3api put-bucket-versioning \
  --bucket "$TF_STATE_BUCKET" \
  --versioning-configuration Status=Enabled

aws s3api put-bucket-encryption \
  --bucket "$TF_STATE_BUCKET" \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

aws s3api put-public-access-block \
  --bucket "$TF_STATE_BUCKET" \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

### How to provision infrastructure

```bash
# After configuring AWS CLI credentials in your dev profile, export it:
export AWS_PROFILE=admin_awslabs  # admin_awslabs is the dev profile name
terraform init
terraform plan
```