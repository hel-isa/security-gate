# Architecture - Security Gate (v2)

## Overview
Version 2 is built around a **product-level reusable GitHub Actions workflow** backed by modular controls. Approved repositories call one gate workflow, choose a preset, and receive standardized scan artifacts plus a dashboard.

## Workflow Design
- `reusable-security-gate.yml`: product entry point for approved repositories.
- `security-baseline.yml`: local workflow used by this repository to run the gate against itself.
- `reusable-secrets.yml`: Gitleaks scan for secret exposure.
- `reusable-sast.yml`: Semgrep scan for static code risks.
- `reusable-sca.yml`: OSV-Scanner scan for vulnerable dependencies.
- `reusable-sbom.yml`: Syft SBOM generation in CycloneDX JSON.
- `reusable-dashboard.yml`: report aggregation and static dashboard creation.

Most repositories should call `reusable-security-gate.yml`. Each lower-level control is still callable through `workflow_call`, enabling advanced repositories to consume any subset of controls.

## Product Presets

The gate exposes a small preset surface:

- `mode: audit` or `mode: non-strict` runs all controls and reports findings without blocking.
- `mode: strict` runs the same baseline and fails when blocking controls detect findings.
- `semgrep_config: auto` keeps SAST language-aware without requiring per-language setup.

This keeps the default path language-agnostic while preserving escape hatches for custom policy.

## Artifact Flow
1. Each control writes machine-readable JSON into `reports/`.
2. Each control uploads artifacts:
   - `gitleaks-report`
   - `semgrep-report`
   - `osv-report`
   - `sbom-report`
3. Dashboard workflow downloads `*-report` artifacts.
4. Dashboard workflow checks out the Security Gate repository assets through `gate_repository` and `gate_ref`.
5. Dashboard workflow normalizes findings with Python and packages a static dashboard artifact.

## Approved Repository Flow

1. A repository owner copies an example workflow into `.github/workflows/security-gate.yml`.
2. The workflow calls `hel-isa/security-gate/.github/workflows/reusable-security-gate.yml@v2`.
3. The first run should use audit mode to establish a baseline.
4. The repository can switch to strict mode when findings are understood and enforcement is accepted.

## Why Separate Runners Are Not Required for v2
- GitHub-hosted runners are enough for baseline scans.
- Runtime is acceptable for most small/medium repositories.
- Artifact handoff provides sufficient inter-job communication.
- Operational complexity is lower than multi-runner/self-hosted setups.

This design is intentionally simple, portable, and extensible.
