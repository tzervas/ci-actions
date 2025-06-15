import os
import re
import sys


def check_for_secrets(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r") as f:
                    content = f.read()
                    if re.search(r"password|secret|api_key", content, re.IGNORECASE):
                        print(f"Potential secret found in {file}")
                        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_compliance.py <source-dir>")
        sys.exit(1)
    if not check_for_secrets(sys.argv[1]):
        sys.exit(1)
