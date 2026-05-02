# External Company Rollout

Use this guide when an approved repository belongs to another company or GitHub organization.

## Recommended Options

Choose one access model before adding the workflow to the target repository.

| Option | Best for | Notes |
| --- | --- | --- |
| Public Security Gate repo | Open/shared baseline | The external company can call the reusable workflow directly. |
| Company-owned fork or mirror | Private customer/company use | The company owns the workflow copy and pins its own release tag. |
| Private same-organization repo | Internal use only | GitHub private reusable workflow sharing is designed for repositories in the same organization. |

For another company, the most practical private model is a fork or mirror inside their GitHub organization.

## Prerequisites

1. Create and push a stable release tag in the Security Gate repo, for example `v2.0.0`.
2. Confirm the target repository allows GitHub Actions and reusable workflows.
3. Start with `deploy_pages: false` to avoid GitHub Pages environment protection issues.
4. Start with `mode: audit` so the first run reports findings without blocking the team.

## If They Call This Repository Directly

Use this only if `hel-isa/security-gate` is public or otherwise accessible to the target repository.

Create `.github/workflows/security-gate.yml` in the external repository:

```yaml
name: Security Gate

on:
  pull_request:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  security-gate:
    name: Security Gate
    uses: hel-isa/security-gate/.github/workflows/reusable-security-gate.yml@v2.0.0
    with:
      mode: audit
      semgrep_config: auto
      repo_name: ${{ github.repository }}
      gate_repository: hel-isa/security-gate
      gate_ref: v2.0.0
      deploy_pages: false
```

## If They Use Their Own Fork or Mirror

This is the recommended private cross-company setup.

1. Fork or mirror this repository into the company's GitHub organization.
2. Create the same stable release tag in that fork or mirror, for example `v2.0.0`.
3. Use the company-owned repository in both `uses` and `gate_repository`.

```yaml
name: Security Gate

on:
  pull_request:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  security-gate:
    name: Security Gate
    uses: COMPANY-ORG/security-gate/.github/workflows/reusable-security-gate.yml@v2.0.0
    with:
      mode: audit
      semgrep_config: auto
      repo_name: ${{ github.repository }}
      gate_repository: COMPANY-ORG/security-gate
      gate_ref: v2.0.0
      deploy_pages: false
```

## First Run Checklist

1. Open a pull request in the external repository.
2. Confirm the jobs run in audit mode.
3. Download the `security-dashboard` artifact.
4. Review Semgrep, Gitleaks, OSV, and SBOM output with the repository owner.
5. Add local allowlists or ignores only when the repository owner accepts the reason.
6. Switch to `mode: strict` only after findings are triaged.

## Common Failures

### Reusable workflow is not found

Check that:

- the Security Gate repo is public or accessible to the caller
- the tag exists, for example `v2.0.0`
- the workflow path is exactly `.github/workflows/reusable-security-gate.yml`

### Dashboard asset checkout fails

Check that `gate_repository` and `gate_ref` point to an accessible Security Gate repo and tag.

### GitHub Pages deployment is rejected

Keep `deploy_pages: false`. The dashboard artifact is still generated. Enable Pages only after the target repository's `github-pages` environment rules are configured.

### Strict mode fails immediately

Use `mode: audit` for onboarding. Strict mode is intentionally blocking when findings are detected.
