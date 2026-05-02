# Security Gate Presets

Presets are lightweight workflow settings. They keep onboarding simple while still allowing teams to tune the gate over time.

## Audit Preset

Use audit mode first for most repositories.

```yaml
with:
  mode: audit
  semgrep_config: auto
```

Audit mode runs:

- Gitleaks secrets detection
- Semgrep SAST with language-aware defaults
- OSV-Scanner dependency vulnerability checks
- Syft SBOM generation
- dashboard aggregation

Findings are reported but do not block the workflow.

## Strict Preset

Use strict mode when the repository is ready for enforcement.

```yaml
with:
  mode: strict
  semgrep_config: auto
```

Strict mode runs the same language-agnostic baseline and fails the gate when findings are detected by blocking controls.

Before switching to strict mode, run audit mode first and review the dashboard artifact. Strict mode is intentionally blocking: if Semgrep reports findings, the SAST job exits with failure until the findings are fixed, suppressed with repository-owned configuration, or accepted through a documented policy.

## Custom Policy Preset

Use this when a repository needs stronger Semgrep rules or local Gitleaks tuning.

```yaml
with:
  mode: strict
  semgrep_config: p/ci
  gitleaks_config_path: .security/gitleaks.toml
```

Recommended local files:

- `.security/gitleaks.toml` for allowlists and repository-specific secret patterns
- `.semgrepignore` for generated code or vendored folders
- repository documentation for accepted risk decisions

## Language-Agnostic Baseline

The default gate avoids language-specific setup:

- Gitleaks scans repository content for secrets.
- Semgrep `auto` selects rules based on detected languages.
- OSV-Scanner recursively detects supported manifests and lockfiles.
- Syft generates an SBOM from the repository path.

Teams can add language-specific policies later without changing the default adoption path.
