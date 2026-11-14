"""Report Python dependency vulnerability counts from pip-audit JSON.

Do not infer safety from a missing report. The security workflow will make
the audit blocking after dependency upgrades and baseline triage.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def summarise(path: str) -> list[tuple[str, str, int]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = []
    for dependency in data.get("dependencies", []):
        vulnerabilities = dependency.get("vulns", [])
        if vulnerabilities:
            rows.append((str(dependency["name"]), str(dependency["version"]), len(vulnerabilities)))
    return sorted(rows, key=lambda row: row[0].lower())


if __name__ == "__main__":
    findings = summarise(sys.argv[1])
    print(f"Packages with reported vulnerabilities: {len(findings)}")
    print(f"Total known findings: {sum(row[2] for row in findings)}")
    for name, version, count in findings:
        print(f"  {name} {version}: {count}")
