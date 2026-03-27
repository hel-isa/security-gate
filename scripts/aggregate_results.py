#!/usr/bin/env python3
"""Normalize security scanner output into a common schema."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate security reports.")
    parser.add_argument("--input-dir", required=True, help="Directory containing raw JSON reports")
    parser.add_argument("--output-file", required=True, help="Path to write normalized JSON")
    parser.add_argument("--repo-name", required=True, help="Repository name")
    return parser.parse_args()


def to_iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def normalize_gitleaks(repo: str, path: Path, scan_date: str) -> list[dict[str, Any]]:
    entries = read_json(path, [])
    findings = []
    for item in entries if isinstance(entries, list) else []:
        findings.append(
            {
                "repo": repo,
                "tool": "gitleaks",
                "category": "secrets",
                "severity": "high",
                "title": item.get("Description", "Potential secret exposed"),
                "file": item.get("File", "unknown"),
                "line": item.get("StartLine", 0),
                "rule_id": item.get("RuleID", "gitleaks-rule"),
                "status": "open",
                "scan_date": scan_date,
            }
        )
    return findings


def normalize_semgrep(repo: str, path: Path, scan_date: str) -> list[dict[str, Any]]:
    data = read_json(path, {"results": []})
    findings = []
    for item in data.get("results", []) if isinstance(data, dict) else []:
        extra = item.get("extra", {})
        severity = str(extra.get("severity", "medium")).lower()
        start = item.get("start", {})
        findings.append(
            {
                "repo": repo,
                "tool": "semgrep",
                "category": "sast",
                "severity": severity,
                "title": extra.get("message", "Semgrep finding"),
                "file": item.get("path", "unknown"),
                "line": start.get("line", 0),
                "rule_id": item.get("check_id", "semgrep-rule"),
                "status": "open",
                "scan_date": scan_date,
            }
        )
    return findings


def normalize_osv(repo: str, path: Path, scan_date: str) -> list[dict[str, Any]]:
    data = read_json(path, {"results": []})
    findings = []
    for result in data.get("results", []) if isinstance(data, dict) else []:
        packages = result.get("packages", []) or []
        for package in packages:
            package_name = (
                package.get("package", {})
                .get("name")
                if isinstance(package, dict)
                else "unknown-package"
            )
            vulns = package.get("vulnerabilities", []) if isinstance(package, dict) else []
            for vuln in vulns:
                findings.append(
                    {
                        "repo": repo,
                        "tool": "osv-scanner",
                        "category": "sca",
                        "severity": "high",
                        "title": vuln.get("summary")
                        or vuln.get("id", "Vulnerable dependency"),
                        "file": result.get("source", {}).get("path", "dependency-manifest"),
                        "line": 0,
                        "rule_id": vuln.get("id", "osv-id"),
                        "status": "open",
                        "scan_date": scan_date,
                        "dependency": package_name,
                    }
                )
    return findings


def sbom_generated(path: Path) -> bool:
    data = read_json(path, {})
    return isinstance(data, dict) and bool(data)


def build_summary(findings: list[dict[str, Any]], sbom_exists: bool, scan_date: str) -> dict[str, Any]:
    tool_counter = Counter(item["tool"] for item in findings)
    severity_counter = Counter(item["severity"] for item in findings)

    return {
        "total_findings": len(findings),
        "findings_by_tool": dict(tool_counter),
        "findings_by_severity": dict(severity_counter),
        "secrets_findings_count": tool_counter.get("gitleaks", 0),
        "vulnerable_dependencies_count": tool_counter.get("osv-scanner", 0),
        "sbom_generated": sbom_exists,
        "latest_scan_date": scan_date,
    }


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_file = Path(args.output_file)

    scan_date = to_iso_now()

    findings: list[dict[str, Any]] = []
    findings.extend(normalize_gitleaks(args.repo_name, input_dir / "gitleaks-report.json", scan_date))
    findings.extend(normalize_semgrep(args.repo_name, input_dir / "semgrep-report.json", scan_date))
    findings.extend(normalize_osv(args.repo_name, input_dir / "osv-report.json", scan_date))

    summary = build_summary(findings, sbom_generated(input_dir / "sbom-cyclonedx.json"), scan_date)

    output = {
        "repo": args.repo_name,
        "scan_date": scan_date,
        "summary": summary,
        "findings": findings,
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote aggregated dashboard data to {output_file}")


if __name__ == "__main__":
    main()
