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


### How to signup and request JWT Tokens for testing

```bash
# Once you have provisioned the userpool, you can create a user and request JWT tokens:
USERPOOL_ID=$(terraform output -raw cognito_user_pool_id)
CLIENT_ID=$(terraform output -raw cognito_app_client_id)
USER_PASSWORD="<Super1Secret!>"

# Create the user:
aws cognito-idp sign-up --client-id "$CLIENT_ID" --username testuser1 --password "$USER_PASSWORD"
{                                                                                                           
    "UserConfirmed": false,
    "UserSub": "448804e8-7011-700b-f132-5d3dd69046bd"
}

# Confirm the user from admin side, skips email verification
aws cognito-idp admin-confirm-sign-up --user-pool-id "$USERPOOL_ID" --username testuser1

# Initialize authentication and fetch the JWT tokens:
ACCESS_TOKEN=$(aws cognito-idp initiate-auth \
  --client-id "$CLIENT_ID" \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME="testuser1",PASSWORD="$USER_PASSWORD" \
  --query 'AuthenticationResult.AccessToken' \
  --output text)