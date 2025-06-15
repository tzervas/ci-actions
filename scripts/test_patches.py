"""
Applies patches from a JSON file and tests their effectiveness using a specified command.
Args:
    patch_file (str): Path to the JSON file containing patch information. 
                        Each patch should include an "action" (command to apply the patch) 
                        and a "vulnerability_id" (identifier for the vulnerability being patched).
    test_command (str): Command to execute after applying each patch to verify its effectiveness.
Raises:
    subprocess.CalledProcessError: If the patch application or testing command fails.
    SystemExit: Exits the program with status code 1 if any patch fails.
Example:
    Given a JSON file `patches.json` with the following content:
    [
        {"action": "patch apply patch1.diff", "vulnerability_id": "CVE-1234"},
        {"action": "patch apply patch2.diff", "vulnerability_id": "CVE-5678"}
    ]
    And a test command `pytest tests/`, the function can be called as:
    test_patches("patches.json", "pytest tests/")
"""
import json
import subprocess
import sys


def test_patches(patch_file, test_command):
    with open(patch_file, "r", encoding="utf-8") as f:
        patches = json.load(f)

    for patch in patches:
        action = patch.get("action")
        vuln_id = patch.get("vulnerability_id")
        print(f"Applying patch for {vuln_id}: {action}")
        try:
            subprocess.run(action.split(), check=True)
            print(f"Testing after applying patch: {test_command}")
            subprocess.run(test_command, check=True)
            print(f"Patch for {vuln_id} passed tests")
        except subprocess.CalledProcessError as e:
            print(f"Patch for {vuln_id} failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_patches.py <patch-suggestions.json> <test-command>")
        sys.exit(1)
    test_patches(sys.argv[1], sys.argv[2:])
