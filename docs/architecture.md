# Architecture - Security Guardrails as a Service (v1)

## Overview
Version 1 is built around **modular reusable GitHub Actions workflows**. Each security control executes independently, produces JSON output, and publishes artifacts. A dedicated dashboard workflow pulls those artifacts and produces normalized reporting.

## Workflow Design
- `reusable-secrets.yml`: Gitleaks scan for secret exposure.
- `reusable-sast.yml`: Semgrep scan for static code risks.
- `reusable-sca.yml`: OSV-Scanner scan for vulnerable dependencies.
- `reusable-sbom.yml`: Syft SBOM generation in CycloneDX JSON.
- `reusable-dashboard.yml`: report aggregation and static dashboard creation.
- `security-baseline.yml`: orchestrator that calls each reusable workflow.

Each control is callable through `workflow_call`, enabling future repositories to consume any subset of controls.

## Artifact Flow
1. Each control writes machine-readable JSON into `reports/`.
2. Each control uploads artifacts:
   - `gitleaks-report`
   - `semgrep-report`
   - `osv-report`
   - `sbom-report`
3. Dashboard workflow downloads `*-report` artifacts, normalizes findings with Python, and packages a static dashboard artifact.

## Why Separate Runners Are Not Required for v1
- GitHub-hosted runners are enough for baseline scans.
- Runtime is acceptable for most small/medium repositories.
- Artifact handoff provides sufficient inter-job communication.
- Operational complexity is lower than multi-runner/self-hosted setups.

This design is intentionally simple, portable, and extensible.
