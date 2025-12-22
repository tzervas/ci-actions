# CI Actions

This repository contains **reusable, composable, and parameterized** GitHub Actions workflows and composite actions for CI/CD tasks across multiple languages and platforms. Built for flexibility, security, and ease of use.

**This project is in early phases of active development, all contents are subject to arbitrary change without notice at this time.**

## Features

- 🚀 **Multi-language support**: Python, Rust, Node.js, Go
- 🏗️ **Composable workflows**: Mix and match reusable components
- 🔒 **Security-first**: Built-in vulnerability scanning and security checks
- 🌐 **Multi-architecture**: Support for amd64, arm64, and cross-compilation
- 📦 **Docker integration**: Build, scan, and push multi-arch images
- 🧪 **Comprehensive testing**: Unit, integration, and coverage reporting
- 📊 **Rich reporting**: Automated summaries and metrics

## Composite Actions

Reusable setup actions that can be used in any workflow:

### Language & Environment Setup
- **setup-python-uv**: Setup Python with uv package manager
- **setup-rust**: Setup Rust toolchain with caching
- **setup-node**: Setup Node.js with package manager support
- **setup-docker-buildx**: Setup Docker Buildx with QEMU for multi-arch

### Utilities
- **report-metrics**: Generate build metrics and system resource reports
- **run-security-scan**: Run security scans using Trivy and/or Snyk

## Reusable Workflows

### Core Workflows

#### `reusable-setup.yml`
Universal language setup and dependency installation workflow.

**Supported Languages**: Python (pip, uv), Rust, Node.js (npm, yarn, pnpm), Go

**Example**:
```yaml
jobs:
  setup:
    uses: tzervas/ci-actions/.github/workflows/reusable-setup.yml@Dev
    with:
      language: python
      language-version: '3.12'
      package-manager: uv
```

#### `reusable-quality-checks.yml`
Code quality checks including linting, formatting, and type checking.

**Features**: Language-specific linters, formatters, syntax validation

**Example**:
```yaml
jobs:
  quality:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: rust
      checks: 'lint,format'
```

#### `reusable-test.yml`
Comprehensive testing with matrix support and coverage reporting.

**Features**: Multi-version testing, code coverage, artifact upload

**Example**:
```yaml
jobs:
  test:
    uses: tzervas/ci-actions/.github/workflows/reusable-test.yml@Dev
    with:
      language: python
      coverage-enabled: true
      upload-coverage: true
      matrix-strategy: |
        {
          "python-version": ["3.10", "3.11", "3.12"]
        }
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

#### `reusable-docker-build.yml`
Build and push multi-architecture Docker images.

**Features**: Multi-platform builds, registry support, automatic scanning

**Example**:
```yaml
jobs:
  docker:
    uses: tzervas/ci-actions/.github/workflows/reusable-docker-build.yml@Dev
    with:
      image-name: 'my-app'
      platforms: 'linux/amd64,linux/arm64'
      push: true
      scan-image: true
    secrets:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### `reusable-security-scan.yml`
Comprehensive security scanning for code, dependencies, and containers.

**Features**: Trivy, Snyk, SARIF upload to GitHub Security

**Example**:
```yaml
jobs:
  security:
    uses: tzervas/ci-actions/.github/workflows/reusable-security-scan.yml@Dev
    with:
      scan-targets: 'all'
      container-image: 'ghcr.io/user/image:latest'
      severity-threshold: 'HIGH'
```

#### `reusable-multiarch-build.yml`
Build and test across multiple architectures (amd64, arm64).

**Features**: QEMU support, cross-compilation, architecture-specific artifacts

**Example**:
```yaml
jobs:
  multiarch:
    uses: tzervas/ci-actions/.github/workflows/reusable-multiarch-build.yml@Dev
    with:
      language: rust
      architectures: 'amd64,arm64'
      artifact-name: 'binaries'
```

### Legacy Workflows

These workflows are maintained for backwards compatibility:

- **python-lint.yml**: Python linting (use `reusable-quality-checks.yml` instead)
- **python-test.yml**: Python testing (use `reusable-test.yml` instead)
- **docker-build.yml**: Docker builds (use `reusable-docker-build.yml` instead)
- **vulnerability-scan.yml**: Security scanning (use `reusable-security-scan.yml` instead)

## Quick Start

### Basic Python CI

```yaml
name: CI

on: [push, pull_request]

jobs:
  quality:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: python
      checks: 'lint,format'

  test:
    needs: quality
    uses: tzervas/ci-actions/.github/workflows/reusable-test.yml@Dev
    with:
      language: python
      coverage-enabled: true
```

### Complete CI/CD Pipeline

See [examples/workflow-compositions.md](examples/workflow-compositions.md) for comprehensive examples including:
- Multi-language projects
- Docker image builds
- Multi-architecture builds
- Security scanning
- Complete CI/CD pipelines

## Usage Tips

1. **Always specify a version**: Use `@Dev` or `@main` or a specific commit SHA
2. **Store secrets properly**: Use GitHub Secrets for sensitive data
3. **Compose workflows**: Chain multiple reusable workflows for complex pipelines
4. **Customize parameters**: All workflows support extensive customization
5. **Review examples**: Check the `examples/` directory for real-world patterns

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE).

## Contact

Reach out via [GitHub Issues](https://github.com/tzervas/ci-actions/issues) or [X](https://x.com/vec_wt_tech).
