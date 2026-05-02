# Security Policy

## Reporting a Vulnerability
Please report vulnerabilities privately via your organization's designated security channel (for example, security@company.com or a private issue template).

Include:
- Affected component(s)
- Reproduction steps
- Potential impact
- Suggested remediation (if known)

## Supported Scope (v2)
This repository provides a reusable CI security gate for approved repositories:
- Secrets detection (Gitleaks)
- SAST (Semgrep)
- SCA (OSV-Scanner)
- SBOM generation (Syft)
- Static dashboard artifacts

## Out of Scope
- Runtime protection
- Cloud workload posture management
- Proprietary GHAS-only features
- Approval management for consuming repositories

## Disclosure Expectations
- Do not publicly disclose vulnerabilities before triage.
- We aim to acknowledge reports within 5 business days.
