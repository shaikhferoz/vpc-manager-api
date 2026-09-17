### How to provision infrastructure

- Here the directory structure `dev` represents the `dev` environment.
- Ensure you have configured the required AWS_profile that is able to talk to AWS APIs from wherever you are running the TF plan/apply.
- Minimally, we will export the configured profile `export AWS_PROFILE=admin_awslab`, before running the TF commands.
- Since this is the `root` module calling the lambda `child` module, all TF commands shall be executed from this directory.