# Changelog

## v2.0.1 - Cross-Repository Reusable Workflow Fix

Patch release for approved repositories that call Security Gate from another repository or organization.

### Fixed

- Made `.github/workflows/reusable-security-gate.yml` self-contained so external consumers do not need local copies of lower-level reusable workflows.
- Prevented GitHub from resolving nested `./.github/workflows/reusable-*.yml` references against the caller repository.

### Release Notes

Approved consumers should pin both the reusable workflow reference and `gate_ref` to `v2.0.1`.

## v2.0.0 - Initial Product Release

Stable release for approved repositories that need a reusable Security Gate workflow.

### Added

- Product-level reusable workflow: `.github/workflows/reusable-security-gate.yml`.
- Audit and strict presets through the `mode` input.
- Copy-paste consumer workflow examples for audit and strict rollout.
- Onboarding, preset, and architecture documentation for approved consumers.
- Dashboard asset checkout through `gate_repository` and `gate_ref` so consumers do not need local dashboard scripts.

### Release Notes

`v2.0.0` should be replaced with `v2.0.1` for external consumers because the product workflow in `v2.0.0` used nested relative reusable workflows.
