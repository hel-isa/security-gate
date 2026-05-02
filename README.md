# Security Gate (v2)

A GitHub-native, reusable security gate that lets approved repositories scan code with a practical default workflow. It uses free/open-source tools and does **not** depend on GitHub Advanced Security.

## Project Purpose
Security Gate provides a productized starting point for security checks in CI:

- one default workflow users can call remotely
- audit and strict presets for non-blocking or blocking scans
- language-agnostic baseline controls
- optional low-level reusable workflows for advanced teams
- standardized JSON artifacts and lightweight dashboard reporting

## Architecture at a Glance
- Product entry point: `.github/workflows/reusable-security-gate.yml`
- Local baseline workflow: `.github/workflows/security-baseline.yml`
- Independent reusable controls:
  - `reusable-secrets.yml` (Gitleaks)
  - `reusable-sast.yml` (Semgrep)
  - `reusable-sca.yml` (OSV-Scanner)
  - `reusable-sbom.yml` (Syft)
  - `reusable-dashboard.yml` (aggregation + static dashboard)

Detailed design is documented in `docs/architecture.md`.

## Supported Tools
- Secrets detection: Gitleaks
- SAST: Semgrep
- SCA: OSV-Scanner
- SBOM: Syft (CycloneDX JSON)

## Quick Start for Approved Repositories

Copy one of the templates from `examples/` into the target repository as `.github/workflows/security-gate.yml`.

Start in audit mode:

```yaml
jobs:
  security-gate:
    name: Security Gate
    uses: hel-isa/security-gate/.github/workflows/reusable-security-gate.yml@v2.0.0
    with:
      mode: audit
      semgrep_config: auto
      repo_name: ${{ github.repository }}
      gate_ref: v2.0.0
```

Switch to strict mode when the team is ready to block on findings:

```yaml
with:
  mode: strict
  semgrep_config: auto
```

See `docs/onboarding.md` for the full copy-paste workflow, `docs/presets.md` for preset guidance, and `docs/release-management.md` for stable tag usage.

## Repository Layout
- `.github/workflows/` - orchestrator and reusable workflow modules
- `examples/` - copy-paste workflows for consuming repositories
- `scripts/` - Python helpers for normalization/dashboard packaging
- `dashboard/` - static dashboard assets (HTML/CSS/JS)
- `docs/` - architecture and secure coding baseline docs
- `.gitleaks.toml` - local gitleaks config
- `SECURITY.md` - vulnerability reporting + scope
- `pull_request_template.md` - secure review checklist

## Presets

| Preset | Mode | Behavior |
| --- | --- | --- |
| Audit | `audit` | Runs scans and reports findings without blocking merges. |
| Strict | `strict` | Runs scans and fails when blocking findings are detected. |

`non-strict` is accepted as an alias for `audit`.

## Artifacts and Dashboard
Each control uploads artifacts in JSON format:
- `gitleaks-report`
- `semgrep-report`
- `osv-report`
- `sbom-report`

The dashboard workflow downloads artifacts, normalizes results into `dashboard-data.json`, and publishes a `security-dashboard` artifact containing:
- `index.html`
- `style.css`
- `app.js`
- `dashboard-data.json`

Open `index.html` locally from the dashboard artifact folder to view the report.

## Advanced Usage

Advanced teams can call individual reusable workflows directly when they need custom composition. Most repositories should use `reusable-security-gate.yml`.

## Stable Releases

Approved consumers should pin to immutable release tags such as `v2.0.0`. Keep the workflow reference and `gate_ref` aligned so the reusable workflow and dashboard assets come from the same release.

## Local Usage (where applicable)
- Aggregation script:
  ```bash
  python scripts/aggregate_results.py --input-dir reports/raw --output-file reports/normalized/dashboard-data.json --repo-name your/repo
  ```
- Dashboard packaging:
  ```bash
  python scripts/generate_dashboard.py --data-file reports/normalized/dashboard-data.json --dashboard-dir dashboard --output-dir reports/dashboard
  ```

## Roadmap Ideas (v2+)
- Severity mapping improvements for OSV and custom policies
- Trend history across runs
- Multi-repo rollup dashboards
- SARIF export option
- Optional Slack/Teams notifications
- v3 bot to inspect repositories and generate tuned workflow/configuration
