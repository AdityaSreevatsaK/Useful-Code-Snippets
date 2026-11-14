"""Regression tests for the security audit summary formatter."""

import json

from scripts.summarise_dependency_audit import summarise


def test_summary_reports_only_vulnerable_packages(tmp_path):
    report = tmp_path / "report.json"
    report.write_text(
        json.dumps({"dependencies": [
            {"name": "safe", "version": "1.0", "vulns": []},
            {"name": "old", "version": "0.1", "vulns": [{"id": "TEST-1"}, {"id": "TEST-2"}]},
        ]}),
        encoding="utf-8",
    )
    assert summarise(str(report)) == [("old", "0.1", 2)]


def test_empty_report(tmp_path):
    report = tmp_path / "report.json"
    report.write_text('{"dependencies":[]}', encoding="utf-8")
    assert summarise(str(report)) == []
