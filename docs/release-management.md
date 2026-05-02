# Release Management

Security Gate consumers should pin to stable release tags. This keeps approved repositories protected from unexpected workflow changes.

## Tag Strategy

Use semantic version tags for immutable releases:

- `v2.0.1`: exact release, recommended for approved consumers
- `v2.0.2`: patch release for compatible fixes
- `v2.1.0`: minor release for compatible features or new optional inputs
- `v3.0.0`: breaking release

The `v2` branch may continue to track active v2 development. Do not ask approved consumers to depend on `@v2` unless they explicitly accept moving updates.

## Consumer Pinning

Approved repositories should pin the reusable workflow and dashboard assets to the same release:

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

## Release Checklist

1. Update `VERSION`.
2. Update `CHANGELOG.md`.
3. Run local validation:

   ```bash
   ruby -e 'require "yaml"; Dir[".github/workflows/*.yml", "examples/*.yml"].each { |f| YAML.load_file(f) }; puts "workflow yaml parse ok"'
   PYTHONPYCACHEPREFIX=/private/tmp/security-gate-pycache python3 -m py_compile scripts/aggregate_results.py scripts/generate_dashboard.py
   ```

4. Commit the release changes.
5. Create an annotated tag:

   ```bash
   git tag -a v2.0.1 -m "Release v2.0.1"
   ```

6. Push the branch and tag:

   ```bash
   git push origin v2
   git push origin v2.0.1
   ```

7. Ask one approved repository to run the audit template before announcing the release more broadly.

## Compatibility Promise

Patch releases should not break existing approved consumers.

Minor releases may add optional inputs or new artifacts, but should preserve existing input names, artifact names, and default behavior.

Major releases may change workflow contracts, artifact schemas, or enforcement behavior.
