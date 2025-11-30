#!/usr/bin/env python3
"""Generate standardized JSON report from semgrep output."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_semgrep_json(path: Path) -> dict:
    """Load semgrep JSON report."""
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def generate_report(job_name: str, semgrep_json_path: Path, duration: float) -> dict:
    """Generate standardized report from semgrep data."""
    semgrep_data = load_semgrep_json(semgrep_json_path)

    # Extract findings
    results = semgrep_data.get("results", [])
    findings = []
    severity_counts = {"critical": 0, "error": 0, "warning": 0, "info": 0}

    for result in results:
        severity = result.get("extra", {}).get("severity", "info").lower()
        if severity in severity_counts:
            severity_counts[severity] += 1

        findings.append({
            "rule_id": result.get("check_id", "unknown"),
            "severity": severity,
            "file": result.get("path", "unknown"),
            "line": result.get("start", {}).get("line", 0),
            "message": result.get("extra", {}).get("message", "No message")
        })

    # Determine status (fail if any errors)
    status = "failure" if (severity_counts["critical"] > 0 or severity_counts["error"] > 0) else "success"

    return {
        "job_name": job_name,
        "status": status,
        "duration_seconds": int(duration),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": {
            "tests": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "failures": []
            },
            "coverage": {
                "total_percent": 0,
                "files": {}
            },
            "security": {
                "findings": findings,
                "severity_counts": severity_counts
            }
        }
    }


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <job_name> <semgrep_json> <duration>")
        sys.exit(1)

    job_name = sys.argv[1]
    semgrep_json_path = Path(sys.argv[2])
    duration = float(sys.argv[3])

    report = generate_report(job_name, semgrep_json_path, duration)

    # Write to results.json
    output_path = Path("results.json")
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    main()
