# Example Workflow Compositions

This directory contains examples of how to compose the reusable workflows for different use cases.

## Python Project with uv

```yaml
name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  quality-checks:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: python
      language-version: '3.12'
      checks: 'lint,format,type'
      linter: 'ruff'

  test:
    needs: quality-checks
    uses: tzervas/ci-actions/.github/workflows/reusable-test.yml@Dev
    with:
      language: python
      coverage-enabled: true
      upload-coverage: true
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

  security:
    uses: tzervas/ci-actions/.github/workflows/reusable-security-scan.yml@Dev
    with:
      scan-targets: 'code,dependencies'
      severity-threshold: 'HIGH'
```

## Rust Multi-Architecture Build

```yaml
name: Rust Multi-Arch CI

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  pre-checks:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: rust
      checks: 'lint,format'

  build-test:
    needs: pre-checks
    uses: tzervas/ci-actions/.github/workflows/reusable-multiarch-build.yml@Dev
    with:
      language: rust
      architectures: 'amd64,arm64'
      artifact-name: 'rust-binaries'
      artifact-paths: |
        target/release/your-binary
        target/aarch64-unknown-linux-gnu/release/your-binary

  security-scan:
    uses: tzervas/ci-actions/.github/workflows/reusable-security-scan.yml@Dev
    with:
      scan-targets: 'all'
```

## Docker Image Build and Push

```yaml
name: Docker Build and Deploy

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  quality-checks:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: python
      checks: 'lint,format'

  docker-build:
    needs: quality-checks
    uses: tzervas/ci-actions/.github/workflows/reusable-docker-build.yml@Dev
    with:
      image-name: 'my-app'
      tags: 'latest,${{ github.ref_name }}'
      platforms: 'linux/amd64,linux/arm64'
      push: ${{ github.event_name == 'push' }}
      scan-image: true
    secrets:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Node.js Project

```yaml
name: Node.js CI

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  quality-checks:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: node
      language-version: '20'
      checks: 'lint,format'

  test:
    needs: quality-checks
    uses: tzervas/ci-actions/.github/workflows/reusable-test.yml@Dev
    with:
      language: node
      matrix-strategy: |
        {
          "node-version": ["18", "20", "22"]
        }
      coverage-enabled: true
```

## Go Project

```yaml
name: Go CI

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  quality-checks:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: go
      checks: 'lint,format'

  test:
    needs: quality-checks
    uses: tzervas/ci-actions/.github/workflows/reusable-test.yml@Dev
    with:
      language: go
      coverage-enabled: true
```

## Complete CI/CD Pipeline

```yaml
name: Complete CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
  release:
    types: [ published ]

jobs:
  # Stage 1: Code Quality
  quality:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: python
      checks: 'lint,format,type'

  # Stage 2: Testing
  test:
    needs: quality
    uses: tzervas/ci-actions/.github/workflows/reusable-test.yml@Dev
    with:
      language: python
      coverage-enabled: true
      upload-coverage: true
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

  # Stage 3: Security Scanning
  security:
    needs: quality
    uses: tzervas/ci-actions/.github/workflows/reusable-security-scan.yml@Dev
    with:
      scan-targets: 'all'
      fail-on-findings: false

  # Stage 4: Build Docker Image
  build:
    needs: [test, security]
    uses: tzervas/ci-actions/.github/workflows/reusable-docker-build.yml@Dev
    with:
      image-name: 'my-app'
      platforms: 'linux/amd64,linux/arm64'
      push: ${{ github.event_name == 'push' || github.event_name == 'release' }}
      tags: |
        latest
        ${{ github.sha }}
        ${{ github.ref_name }}
    secrets:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # Stage 5: Container Security Scan
  container-security:
    needs: build
    if: github.event_name == 'push' || github.event_name == 'release'
    uses: tzervas/ci-actions/.github/workflows/reusable-security-scan.yml@Dev
    with:
      scan-targets: 'container'
      container-image: 'ghcr.io/${{ github.repository_owner }}/my-app:latest'
```

## Minimal Setup

For projects that just need basic CI:

```yaml
name: Basic CI

on: [push, pull_request]

jobs:
  ci:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: python
      checks: 'lint'
```
