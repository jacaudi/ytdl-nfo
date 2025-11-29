#!/usr/bin/env python3
"""Generate standardized JSON report from pytest and coverage output."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_pytest_json(path: Path) -> dict:
    """Load pytest JSON report."""
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def load_coverage_json(path: Path) -> dict:
    """Load coverage JSON report."""
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def generate_report(job_name: str, pytest_json_path: Path, coverage_json_path: Path, duration: float) -> dict:
    """Generate standardized report from pytest and coverage data."""
    pytest_data = load_pytest_json(pytest_json_path)
    coverage_data = load_coverage_json(coverage_json_path)

    # Extract test results
    summary = pytest_data.get("summary", {})
    tests_total = summary.get("total", 0)
    tests_passed = summary.get("passed", 0)
    tests_failed = summary.get("failed", 0)
    tests_skipped = summary.get("skipped", 0)

    # Extract failures
    failures = []
    for test in pytest_data.get("tests", []):
        if test.get("outcome") == "failed":
            failures.append({
                "test_name": test.get("nodeid", "unknown"),
                "error_message": test.get("call", {}).get("longrepr", "No error message")
            })

    # Extract coverage
    coverage_percent = coverage_data.get("totals", {}).get("percent_covered", 0)
    coverage_files = {}
    for filename, data in coverage_data.get("files", {}).items():
        coverage_files[filename] = {
            "percent": data.get("summary", {}).get("percent_covered", 0),
            "missing_lines": ",".join(map(str, data.get("missing_lines", [])))
        }

    # Determine status
    status = "success" if tests_failed == 0 else "failure"

    return {
        "job_name": job_name,
        "status": status,
        "duration_seconds": int(duration),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": {
            "tests": {
                "total": tests_total,
                "passed": tests_passed,
                "failed": tests_failed,
                "skipped": tests_skipped,
                "failures": failures
            },
            "coverage": {
                "total_percent": round(coverage_percent, 1),
                "files": coverage_files
            },
            "security": {
                "findings": [],
                "severity_counts": {"error": 0, "warning": 0, "info": 0}
            }
        }
    }


def main():
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <job_name> <pytest_json> <coverage_json> <duration>")
        sys.exit(1)

    job_name = sys.argv[1]
    pytest_json_path = Path(sys.argv[2])
    coverage_json_path = Path(sys.argv[3])
    duration = float(sys.argv[4])

    report = generate_report(job_name, pytest_json_path, coverage_json_path, duration)

    # Write to results.json
    output_path = Path("results.json")
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    main()
