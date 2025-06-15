"""
Deploys infrastructure using Terraform based on the specified environment,
runs the provided test command, and then destroys the deployed infrastructure.

Args:
environment (str): The target environment for deployment. 
                    Accepted values are "aws" or "gcp".
test_command (str): The command to execute tests after deployment. 
                    This should be a string representing the command.

Raises:
subprocess.CalledProcessError: If any of the subprocess commands fail.
"""

import subprocess
import sys


def deploy_and_test(environment, test_command):
    if environment == "aws":
        subprocess.run(
            ["terraform", "apply", "-auto-approve", "-var-file=aws.tfvars"], check=True
        )
    elif environment == "gcp":
        subprocess.run(
            ["terraform", "apply", "-auto-approve", "-var-file=gcp.tfvars"], check=True
        )
    subprocess.run(test_command.split(), check=True)
    subprocess.run(["terraform", "destroy", "-auto-approve"], check=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python deploy_and_test.py <environment> <test-command>")
        sys.exit(1)
    deploy_and_test(sys.argv[1], sys.argv[2])
