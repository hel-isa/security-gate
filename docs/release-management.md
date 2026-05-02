# Release Management

Security Gate consumers should pin to stable release tags. This keeps approved repositories protected from unexpected workflow changes.

## Tag Strategy

Use semantic version tags for immutable releases, plus the `v2` branch for users who want the latest compatible version:

- `v2.0.1`: exact release, recommended for approved consumers
- `v2.0.2`: patch release for compatible fixes
- `v2.1.0`: minor release for compatible features or new optional inputs
- `v2`: moving branch for the latest compatible v2 release
- `v3.0.0`: breaking release

Do not create a `v2` tag while a `v2` branch exists. Keep `v2` as the latest compatible branch.

## Consumer Pinning

Approved repositories should pin the reusable workflow and dashboard assets to the same exact release when they need predictable builds:

```yaml
jobs:
  security-gate:
    name: Security Gate
    uses: hel-isa/security-gate/.github/workflows/reusable-security-gate.yml@v2.0.1
    with:
      mode: audit
      semgrep_config: auto
      repo_name: ${{ github.repository }}
      gate_ref: v2.0.1
```

Keep these aligned:

- workflow reference: `@v2.0.1`
- dashboard/script reference: `gate_ref: v2.0.1`

## Latest Compatible Version

Users who want automatic compatible updates can use the moving `v2` branch:

```yaml
jobs:
  security-gate:
    name: Security Gate
    uses: hel-isa/security-gate/.github/workflows/reusable-security-gate.yml@v2
    with:
      mode: audit
      semgrep_config: auto
      repo_name: ${{ github.repository }}
      gate_ref: v2
```

Use this only when the consumer accepts receiving patch and minor v2 updates automatically. For production or external-company onboarding, exact tags such as `v2.0.1` are safer.

## Pull Request Release Flow

Use a pull request for every release. The release PR should include:

- `VERSION` updated to the next version
- `CHANGELOG.md` updated with the release notes
- examples and docs updated to the new recommended exact tag
- workflow validation results

Suggested branch and PR flow:

```bash
git checkout v2
git pull origin v2
git checkout -b release/v2.0.1
git add .
git commit -m "Prepare v2.0.1 release"
git push origin release/v2.0.1
```

Then open a PR from `release/v2.0.1` into `v2`.

## Release Checklist

1. Update `VERSION`.
2. Update `CHANGELOG.md`.
3. Run local validation:

   ```bash
   ruby -e 'require "yaml"; Dir[".github/workflows/*.yml", "examples/*.yml"].each { |f| YAML.load_file(f) }; puts "workflow yaml parse ok"'
   PYTHONPYCACHEPREFIX=/private/tmp/security-gate-pycache python3 -m py_compile scripts/aggregate_results.py scripts/generate_dashboard.py
   ```

4. Open and merge the release PR into `v2`.
5. Pull the merged `v2` branch:

   ```bash
   git checkout v2
   git pull origin v2
   ```

6. Create an annotated exact release tag:

   ```bash
   git tag -a v2.0.1 -m "Release v2.0.1"
   ```

7. Push the exact tag:

   ```bash
   git push origin v2.0.1
   ```

8. Ask one approved repository to run the audit template before announcing the release more broadly.

If you do not want a moving latest branch, ask all consumers to use exact tags only.

## Compatibility Promise

Patch releases should not break existing approved consumers.

Minor releases may add optional inputs or new artifacts, but should preserve existing input names, artifact names, and default behavior.

Major releases may change workflow contracts, artifact schemas, or enforcement behavior.
