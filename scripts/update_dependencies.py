import subprocess
import sys


def update_dependencies(requirements_file):
    subprocess.run(["pip-upgrader", requirements_file, "--upgrade"], check=True)
    subprocess.run(["pip", "freeze", "> updated_requirements.txt"], check=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_dependencies.py <requirements.txt>")
        sys.exit(1)
    update_dependencies(sys.argv[1])
