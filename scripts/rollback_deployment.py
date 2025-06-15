import subprocess
import sys


def rollback_deployment(deployment_name):
    subprocess.run(
        ["kubectl", "rollout", "undo", f"deployment/{deployment_name}"], check=True
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rollback_deployment.py <deployment-name>")
        sys.exit(1)
    rollback_deployment(sys.argv[1])
