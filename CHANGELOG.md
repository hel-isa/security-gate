# Changelog

## v2.0.0 - Initial Product Release

Stable release for approved repositories that need a reusable Security Gate workflow.

### Added

- Product-level reusable workflow: `.github/workflows/reusable-security-gate.yml`.
- Audit and strict presets through the `mode` input.
- Copy-paste consumer workflow examples for audit and strict rollout.
- Onboarding, preset, and architecture documentation for approved consumers.
- Dashboard asset checkout through `gate_repository` and `gate_ref` so consumers do not need local dashboard scripts.

### Release Notes

Approved consumers should pin both the reusable workflow reference and `gate_ref` to `v2.0.0`.
