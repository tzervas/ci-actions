"""
Generate patch suggestions based on Trivy scan results and Python dependency tree.
This function analyzes the vulnerabilities reported by Trivy in a given scan results file
and generates patch suggestions for each vulnerable package. Additionally, it inspects the
Python dependency tree to suggest updates for dependencies that are part of the patch list.
Args:
    trivy_results_file (str): Path to the JSON file containing Trivy scan results.
    requirements_file (str): Path to the requirements file (currently unused in the function).
Raises:
    subprocess.SubprocessError: If an error occurs while running the `pipdeptree` command.
Outputs:
    A JSON file named `patch-suggestions.json` containing a list of patch suggestions.
    Each suggestion includes:
        - vulnerability_id: The ID of the vulnerability.
        - package: The name of the affected package.
        - suggested_fix: A textual description of the suggested fix.
        - action: The command to apply the suggested fix.
"""
import json
import subprocess
import sys


def generate_patches(trivy_results_file, requirements_file):
    # Load Trivy scan results
    with open(trivy_results_file, "r", encoding="utf-8") as f:
        results = json.load(f)

    patches = []
    for result in results.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            pkg_name = vuln.get("PkgName")
            vuln_id = vuln.get("VulnerabilityID")
            fixed_version = vuln.get("FixedVersion")
            if pkg_name and fixed_version:
                patches.append(
                    {
                        "vulnerability_id": vuln_id,
                        "package": pkg_name,
                        "suggested_fix": f"Update {pkg_name} to {fixed_version}",
                        "action": f"pip install {pkg_name}=={fixed_version}",
                    }
                )

    # Generate dependency updates
    try:
        result = subprocess.run(
            ["pipdeptree", "--json"], capture_output=True, text=True, check=True
        )
        dep_tree = json.loads(result.stdout)
        for dep in dep_tree:
            if dep["package"]["package_name"] in [p["package"] for p in patches]:
                patches.append(
                    {
                        "vulnerability_id": "DEPENDENCY_UPDATE",
                        "package": dep["package"]["package_name"],
                        "suggested_fix": f"Update {dep['package']['package_name']} to latest",
                        "action": f"pip install {dep['package']['package_name']} --upgrade",
                    }
                )
    except subprocess.SubprocessError as e:
        print(f"Error generating dependency updates: {e}")

    # Save patch suggestions
    with open("patch-suggestions.json", "w", encoding="utf-8") as f:
        json.dump(patches, f, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python generate_patches.py <trivy-results.json> <requirements.txt>"
        )
        sys.exit(1)
    generate_patches(sys.argv[1], sys.argv[2])
