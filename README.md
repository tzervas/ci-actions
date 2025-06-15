# CI Actions

This repository contains reusable GitHub Actions workflows for CI/CD tasks in Python projects, with a focus on security and hardening.

**This project is in early phases of active development, all contents are subject to arbitrary change without notice at this time.

## Workflows

- **python-lint.yml**: Lints Python code using Flake8 or other linters.
- **python-test.yml**: Runs tests with `pytest` and uploads coverage to Codecov.
- **deploy-github-runners.yml**: Deploys GitHub Actions runners (cloud or self-hosted).
- **deploy-azure-runners.yml**: Deploys runners on Azure VM Scale Sets.
- **deploy-gcp-runners.yml**: Deploys runners on Google Cloud Compute Engine.
- **container-scan.yml**: Scans Docker images for vulnerabilities using Trivy.
- **release-and-package.yml**: Generates GitHub releases and packages Docker images.
- **host-container.yml**: Pushes images to Docker Hub, Azure Container Registry, or Google Container Registry.
- **vulnerability-scan.yml**: Scans Docker images for vulnerabilities and stores results.
- **patch-generation.yml**: Generates patch suggestions for detected vulnerabilities.
- **patch-review-test.yml**: Applies and tests patches, notifying for manual review if needed.

## Usage

1. Add a workflow file in your project’s `.github/workflows/` directory.
2. Reference a workflow, e.g.:

   ```yaml
   jobs:
     vuln-scan:
       uses: tzervas/ci-actions/.github/workflows/vulnerability-scan.yml@main
       with:
         image-name: tzervas/myapp:latest
   ```

3. Store secrets (e.g., `CODECOV_TOKEN`, `SNYK_TOKEN`) in GitHub Secrets.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE).

## Contact

Reach out via [GitHub Issues](https://github.com/tzervas/ci-actions/issues) or [X](https://x.com/vec_wt_tech).
