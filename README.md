# Security Guardrails as a Service (v1)

A GitHub-native, reusable, modular DevSecOps baseline that uses only free/open-source tools and does **not** depend on GitHub Advanced Security.

## Project Purpose
This project provides a production-minded starting point for security checks in CI:
- modular reusable workflows
- standardized JSON artifacts
- lightweight static dashboard reporting
- Python-based data normalization for extensibility

## Architecture at a Glance
- Orchestrator workflow: `.github/workflows/security-baseline.yml`
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

## Repository Layout
- `.github/workflows/` - orchestrator and reusable workflow modules
- `scripts/` - Python helpers for normalization/dashboard packaging
- `dashboard/` - static dashboard assets (HTML/CSS/JS)
- `docs/` - architecture and secure coding baseline docs
- `.gitleaks.toml` - local gitleaks config
- `SECURITY.md` - vulnerability reporting + scope
- `pull_request_template.md` - secure review checklist

## How to Enable Workflows
1. Push this repository to GitHub.
2. Ensure GitHub Actions are enabled for the repository.
3. Confirm default branch is `main` (or adjust trigger branch in `security-baseline.yml`).
4. Open a PR or push to `main` to trigger scans.

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
