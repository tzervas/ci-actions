# Workflow Architecture

## Overview

This repository provides a comprehensive, composable CI/CD framework built on reusable GitHub Actions workflows and composite actions. The architecture is designed to be:

- **Idempotent**: Workflows produce consistent results regardless of how many times they run
- **Parameterized**: Extensive configuration options for customization
- **Composable**: Mix and match components to build complex pipelines
- **Multi-language**: Support for Python, Rust, Node.js, and Go
- **Security-focused**: Built-in scanning and vulnerability detection

## Architecture Layers

### Layer 1: Composite Actions
Low-level, reusable actions that perform specific setup tasks:

```
.github/actions/
├── setup-python-uv/       # Python + uv package manager
├── setup-rust/            # Rust toolchain + cargo cache
├── setup-node/            # Node.js + npm/yarn/pnpm
├── setup-docker-buildx/   # Docker Buildx + QEMU
├── report-metrics/        # Build metrics reporting
└── run-security-scan/     # Security vulnerability scanning
```

### Layer 2: Reusable Workflows
Higher-level workflows that compose actions and provide complete CI/CD stages:

```
.github/workflows/
├── reusable-setup.yml              # Universal environment setup
├── reusable-quality-checks.yml     # Code quality (lint, format, type)
├── reusable-test.yml               # Testing with matrix support
├── reusable-docker-build.yml       # Multi-arch Docker builds
├── reusable-security-scan.yml      # Comprehensive security scanning
└── reusable-multiarch-build.yml    # Cross-architecture builds
```

### Layer 3: Composed Pipelines
User-defined workflows in consuming repositories that compose Layer 2 workflows.

## Design Patterns

### 1. Matrix-Based Multi-Version Testing

```yaml
jobs:
  test:
    uses: tzervas/ci-actions/.github/workflows/reusable-test.yml@Dev
    with:
      language: python
      matrix-strategy: |
        {
          "python-version": ["3.10", "3.11", "3.12"],
          "os": ["ubuntu-latest", "macos-latest"]
        }
```

### 2. Sequential Pipeline with Dependencies

```yaml
jobs:
  quality:
    uses: ./.github/workflows/reusable-quality-checks.yml
  
  test:
    needs: quality
    uses: ./.github/workflows/reusable-test.yml
  
  security:
    needs: quality
    uses: ./.github/workflows/reusable-security-scan.yml
  
  build:
    needs: [test, security]
    uses: ./.github/workflows/reusable-docker-build.yml
```

### 3. Parallel Execution

```yaml
jobs:
  quality:
    uses: ./.github/workflows/reusable-quality-checks.yml
  
  security-code:
    uses: ./.github/workflows/reusable-security-scan.yml
    with:
      scan-targets: 'code,dependencies'
  
  test:
    uses: ./.github/workflows/reusable-test.yml
```

### 4. Conditional Execution

```yaml
jobs:
  build:
    uses: ./.github/workflows/reusable-docker-build.yml
    with:
      push: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
  
  deploy:
    needs: build
    if: github.event_name == 'release'
    uses: ./.github/workflows/deploy.yml
```

## Common Patterns by Language

### Python with uv

```yaml
jobs:
  ci:
    uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
    with:
      language: python
      language-version: '3.12'
      checks: 'lint,format,type'
```

Key features from codemate-hub:
- uv for fast dependency management
- Syntax validation with compile checks
- Custom linting with ruff/flake8

### Rust Multi-Architecture

```yaml
jobs:
  build:
    uses: tzervas/ci-actions/.github/workflows/reusable-multiarch-build.yml@Dev
    with:
      language: rust
      architectures: 'amd64,arm64'
```

Key features from embeddenator:
- Clippy for linting
- rustfmt for formatting
- Cross-compilation support
- Pre-checks before full builds

### Docker Image Pipeline

```yaml
jobs:
  docker:
    uses: tzervas/ci-actions/.github/workflows/reusable-docker-build.yml@Dev
    with:
      image-name: 'my-app'
      platforms: 'linux/amd64,linux/arm64'
      scan-image: true
```

Key features from embeddenator:
- Multi-platform builds with QEMU
- Automatic vulnerability scanning
- Registry-agnostic (Docker Hub, GHCR, custom)
- Build cache optimization

## Workflow Parameters

### Universal Parameters

Most workflows support these common parameters:

- `working-directory`: Set working directory for all operations
- `timeout-minutes`: Override default timeout
- `fail-on-error`: Control failure behavior (boolean)

### Language-Specific Parameters

#### Python
- `package-manager`: `pip`, `uv`
- `language-version`: e.g., `3.10`, `3.11`, `3.12`
- `linter`: `flake8`, `ruff`, `pylint`
- `formatter`: `black`, `isort`

#### Rust
- `toolchain`: `stable`, `nightly`, `1.70.0`
- `components`: `clippy`, `rustfmt`
- `targets`: `aarch64-unknown-linux-gnu`

#### Node.js
- `package-manager`: `npm`, `yarn`, `pnpm`
- `node-version`: `18`, `20`, `22`

#### Go
- `go-version`: `1.20`, `1.21`, `stable`

## Security Integration

All workflows support security scanning at multiple levels:

### Code-level Security
```yaml
security-scan:
  uses: ./.github/workflows/reusable-security-scan.yml
  with:
    scan-targets: 'code'
```

### Dependency Security
```yaml
security-scan:
  uses: ./.github/workflows/reusable-security-scan.yml
  with:
    scan-targets: 'dependencies'
```

### Container Security
```yaml
security-scan:
  uses: ./.github/workflows/reusable-security-scan.yml
  with:
    scan-targets: 'container'
    container-image: 'ghcr.io/user/app:latest'
```

## Idempotency Guarantees

All workflows are designed to be idempotent:

1. **Setup actions** check for existing installations before installing
2. **Build caching** uses GitHub Actions cache with stable keys
3. **Test results** are deterministic given the same code
4. **Security scans** produce consistent results for the same code/image
5. **Docker builds** use content-addressable storage

## Performance Optimization

### Caching Strategy

1. **Language-level caching**
   - Python: pip cache, uv cache
   - Rust: cargo cache (via Swatinem/rust-cache)
   - Node.js: npm/yarn/pnpm cache
   - Go: module cache

2. **Build caching**
   - Docker: GitHub Actions cache for layers
   - Artifacts: Reuse across jobs

3. **Dependency caching**
   - Smart cache keys based on lock files
   - Automatic cache invalidation

### Parallel Execution

Workflows are designed to run in parallel where possible:
- Quality checks can run parallel to security scans
- Multi-architecture builds use matrix strategy
- Test suites can be split across multiple runners

## Extracted Patterns

### From codemate-hub
- Python + uv setup pattern
- Changelog validation
- Comprehensive preflight checks
- Memory initialization tests
- Pipeline regression testing
- Test result summaries

### From embeddenator
- Multi-architecture Rust builds (amd64, arm64)
- Pre-check workflows before main builds
- Build metrics and system resource reporting
- Holographic OS builds (custom Docker images)
- Nightly build schedules
- Matrix-based OS/version/arch combinations

### From DynEL
- Python logging configuration patterns
- Error handling workflows

### From autogit
- Self-hosted runner patterns
- Automated lifecycle management

### From cowpoke
- Container resource management
- Automated allocation patterns

## Migration Guide

### From Legacy Workflows

If you're using the old workflows:

| Old Workflow | New Workflow | Notes |
|-------------|--------------|-------|
| `python-lint.yml` | `reusable-quality-checks.yml` | More features, multi-language |
| `python-test.yml` | `reusable-test.yml` | Matrix support, more languages |
| `docker-build.yml` | `reusable-docker-build.yml` | Multi-arch, scanning |
| `vulnerability-scan.yml` | `reusable-security-scan.yml` | Comprehensive scanning |

### Update References

Change from:
```yaml
uses: tzervas/ci-actions/.github/workflows/python-lint.yml@main
```

To:
```yaml
uses: tzervas/ci-actions/.github/workflows/reusable-quality-checks.yml@Dev
with:
  language: python
```

## Future Enhancements

Planned additions:
- [ ] Deployment workflows (AWS, Azure, GCP, Kubernetes)
- [ ] Performance profiling workflows
- [ ] Database migration workflows
- [ ] Release management workflows
- [ ] Notification workflows (Slack, Discord, Email)
- [ ] Cost optimization reporting
- [ ] Additional language support (Java, C++, Ruby)
