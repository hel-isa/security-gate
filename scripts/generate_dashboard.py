#!/usr/bin/env python3
"""Prepare static dashboard artifact bundle."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate dashboard artifact bundle.")
    parser.add_argument("--data-file", required=True, help="Normalized JSON data file")
    parser.add_argument("--dashboard-dir", required=True, help="Path to static dashboard assets")
    parser.add_argument("--output-dir", required=True, help="Path to output bundle")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    data_file = Path(args.data_file)
    dashboard_dir = Path(args.dashboard_dir)
    output_dir = Path(args.output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    for asset_name in ["index.html", "style.css", "app.js"]:
        shutil.copy2(dashboard_dir / asset_name, output_dir / asset_name)

    shutil.copy2(data_file, output_dir / "dashboard-data.json")
    print(f"Dashboard artifact generated in {output_dir}")


if __name__ == "__main__":
    main()
