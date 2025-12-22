# Quick Reference Guide

## Composite Actions

### setup-python-uv

Setup Python with uv package manager.

```yaml
- uses: tzervas/ci-actions/.github/actions/setup-python-uv@Dev
  with:
    python-version: '3.12'  # default: '3.12'
    uv-version: '0.7.18'    # default: '0.7.18'
    cache: 'true'           # default: 'true'
```

### setup-rust

Setup Rust toolchain with caching.

```yaml
- uses: tzervas/ci-actions/.github/actions/setup-rust@Dev
  with:
    toolchain: 'stable'     # default: 'stable'
    components: 'clippy,rustfmt'  # optional
    targets: 'aarch64-unknown-linux-gnu'  # optional
    cache-key: 'my-project' # optional
    enable-cache: 'true'    # default: 'true'
```

### setup-node

Setup Node.js with package manager.

```yaml
- uses: tzervas/ci-actions/.github/actions/setup-node@Dev
  with:
    node-version: '20'      # default: '20'
    package-manager: 'npm'  # default: 'npm' (npm/yarn/pnpm)
    cache: 'true'           # default: 'true'
```

### setup-docker-buildx

Setup Docker Buildx with QEMU for multi-arch builds.

```yaml
- uses: tzervas/ci-actions/.github/actions/setup-docker-buildx@Dev
  with:
    platforms: 'linux/amd64,linux/arm64'  # default
    buildx-version: 'latest'              # default: 'latest'
    enable-qemu: 'true'                   # default: 'true'
```

### report-metrics

Generate build metrics report.

```yaml
- uses: tzervas/ci-actions/.github/actions/report-metrics@Dev
  with:
    job-name: 'Build Job'
    architecture: 'amd64'           # optional
    runner: 'ubuntu-latest'         # optional
    include-system-info: 'true'     # default: 'true'
```

### run-security-scan

Run security vulnerability scans.

```yaml
- uses: tzervas/ci-actions/.github/actions/run-security-scan@Dev
  with:
    scan-type: 'trivy'              # trivy/snyk/both
    target: 'filesystem'            # filesystem/image
    target-path: '.'                # default: '.'
    severity: 'HIGH,CRITICAL'       # default
    output-format: 'table'          # table/json/sarif
    fail-on-findings: 'false'       # default: 'false'
```

## Reusable Workflows

### reusable-setup.yml

Universal language setup and dependency installation.

```yaml
jobs:
  setup:
    uses: tzervas/ci-actions/.github/workflows/reusable-setup.yml@Dev
    with:
      language: 'python'              # python/rust/node/go
      language-version: '3.12'        # optional
      package-manager: 'uv'           # optional
      install-command: ''             # optional custom command
      cache-enabled: true             # default: true
      working-directory: '.'          # default: '.'
```

### reusable-quality-checks.yml

Code quality checks (linting, formatting, type checking).

```yaml
jobs:
  quality:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: 'python'              # python/rust/node/go
      language-version: '3.12'        # optional
      checks: 'lint,format,type'      # comma-separated
      linter: 'ruff'                  # optional
      formatter: 'black'              # optional
      fail-on-error: true             # default: true
      working-directory: '.'          # default: '.'
```

### reusable-test.yml

Testing with matrix support and coverage.

```yaml
jobs:
  test:
    uses: tzervas/ci-actions/.github/workflows/reusable-test.yml@Dev
    with:
      language: 'python'              # python/rust/node/go
      test-command: ''                # optional custom command
      test-type: 'all'                # unit/integration/e2e/all
      coverage-enabled: true          # default: true
      coverage-format: 'xml'          # xml/html/lcov
      upload-coverage: false          # default: false
      matrix-strategy: '{}'           # JSON matrix
      timeout-minutes: 30             # default: 30
      working-directory: '.'          # default: '.'
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}  # if upload-coverage
```

**Matrix Strategy Example**:
```yaml
matrix-strategy: |
  {
    "python-version": ["3.10", "3.11", "3.12"],
    "os": ["ubuntu-latest", "macos-latest"]
  }
```

### reusable-docker-build.yml

Multi-architecture Docker image builds.

```yaml
jobs:
  docker:
    uses: tzervas/ci-actions/.github/workflows/reusable-docker-build.yml@Dev
    with:
      dockerfile: 'Dockerfile'        # default: 'Dockerfile'
      context: '.'                    # default: '.'
      image-name: 'my-app'            # REQUIRED
      tags: 'latest,v1.0'             # comma-separated
      platforms: 'linux/amd64'        # comma-separated
      push: false                     # default: false
      registry: 'ghcr.io'             # docker.io/ghcr.io/custom
      build-args: 'KEY=VALUE'         # comma-separated
      cache-enabled: true             # default: true
      scan-image: true                # default: true
    secrets:
      REGISTRY_USERNAME: ${{ secrets.DOCKER_USERNAME }}  # if needed
      REGISTRY_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}  # if needed
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}          # for ghcr.io
```

### reusable-security-scan.yml

Comprehensive security scanning.

```yaml
jobs:
  security:
    uses: tzervas/ci-actions/.github/workflows/reusable-security-scan.yml@Dev
    with:
      scan-targets: 'all'             # code/dependencies/container/all
      container-image: ''             # required if scanning container
      severity-threshold: 'HIGH'      # UNKNOWN/LOW/MEDIUM/HIGH/CRITICAL
      fail-on-findings: false         # default: false
      upload-sarif: true              # default: true
      working-directory: '.'          # default: '.'
    secrets:
      SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}  # optional
```

### reusable-multiarch-build.yml

Build and test across multiple architectures.

```yaml
jobs:
  multiarch:
    uses: tzervas/ci-actions/.github/workflows/reusable-multiarch-build.yml@Dev
    with:
      language: 'rust'                # python/rust/node/go
      architectures: 'amd64,arm64'    # comma-separated
      build-command: ''               # optional custom command
      test-command: ''                # optional custom command
      artifact-name: 'artifacts'      # default
      artifact-paths: ''              # newline-separated paths
      timeout-minutes: 30             # default: 30
```

## Common Patterns

### Minimal CI

```yaml
name: CI
on: [push, pull_request]
jobs:
  ci:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: python
      checks: lint
```

### Python with Tests

```yaml
name: Python CI
on: [push, pull_request]
jobs:
  quality:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: python
      checks: lint,format
  
  test:
    needs: quality
    uses: tzervas/ci-actions/.github/workflows/reusable-test.yml@Dev
    with:
      language: python
      coverage-enabled: true
```

### Rust Multi-Arch

```yaml
name: Rust Build
on: [push]
jobs:
  build:
    uses: tzervas/ci-actions/.github/workflows/reusable-multiarch-build.yml@Dev
    with:
      language: rust
      architectures: amd64,arm64
```

### Docker Build & Push

```yaml
name: Docker
on:
  push:
    branches: [main]
jobs:
  docker:
    uses: tzervas/ci-actions/.github/workflows/reusable-docker-build.yml@Dev
    with:
      image-name: my-app
      platforms: linux/amd64,linux/arm64
      push: true
    secrets:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Complete Pipeline

```yaml
name: Full CI/CD
on: [push]
jobs:
  quality:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: python
      checks: lint,format,type
  
  test:
    needs: quality
    uses: tzervas/ci-actions/.github/workflows/reusable-test.yml@Dev
    with:
      language: python
      coverage-enabled: true
  
  security:
    uses: tzervas/ci-actions/.github/workflows/reusable-security-scan.yml@Dev
    with:
      scan-targets: all
  
  docker:
    needs: [test, security]
    uses: tzervas/ci-actions/.github/workflows/reusable-docker-build.yml@Dev
    with:
      image-name: my-app
      push: ${{ github.ref == 'refs/heads/main' }}
    secrets:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Tips

1. **Always pin to a version**: Use `@Dev`, `@main`, or a commit SHA
2. **Use matrix for multi-version testing**: Reduces duplication
3. **Parallel when possible**: Run quality, security, tests in parallel
4. **Cache aggressively**: All setup actions support caching
5. **Fail fast**: Use `fail-on-error: true` for critical checks
6. **Scan everything**: Enable security scanning for all workflows
7. **Use artifacts**: Share build outputs between jobs
8. **Add summaries**: Enable reporting for visibility

## Troubleshooting

### Action not found
- Ensure you're using the correct ref (`@Dev` or `@main`)
- Check the action path is correct

### Permission denied
- Add required permissions to your workflow:
  ```yaml
  permissions:
    contents: read
    packages: write  # for Docker pushes
    security-events: write  # for SARIF upload
  ```

### Cache not working
- Verify cache keys are stable
- Check if cache size exceeds GitHub limits (10GB)
- Ensure dependencies are in standard locations

### Build timeout
- Increase `timeout-minutes` parameter
- Check for hanging processes
- Review system resources in job logs

### Docker push fails
- Verify registry credentials are correct
- Check `push: true` is set
- Ensure GITHUB_TOKEN has package write permission

## Support

For issues or questions:
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for design details
- Review [examples/](examples/) for more patterns
- Open an issue at https://github.com/tzervas/ci-actions/issues
