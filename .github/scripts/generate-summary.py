#!/usr/bin/env python3
"""Generate GitHub job summary from CI result JSON files."""

import json
import os
from pathlib import Path


def load_results(results_dir: Path) -> list[dict]:
    """Load all result JSON files from directory."""
    results = []

    if not results_dir.exists():
        return results

    for json_file in results_dir.glob("**/*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
                results.append(data)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: Failed to load {json_file}: {e}")

    return results


def format_status(status: str) -> str:
    """Format status with emoji."""
    if status == "success":
        return "✓"
    elif status == "failure":
        return "✗"
    else:
        return "⊘"


def format_duration(seconds: int) -> str:
    """Format duration in human-readable form."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}m {secs}s"


def generate_summary(results: list[dict]) -> str:
    """Generate markdown summary from results."""
    if not results:
        return "# CI Results Summary\n\nNo results available.\n"

    # Header
    md = ["# CI Results Summary\n"]

    # Table
    md.append("| Job | Status | Duration | Tests | Coverage | Security |")
    md.append("|-----|--------|----------|-------|----------|----------|")

    all_success = True

    for result in results:
        job_name = result.get("job_name", "Unknown")
        status = result.get("status", "unknown")
        duration = result.get("duration_seconds", 0)

        status_icon = format_status(status)
        if status != "success":
            all_success = False

        duration_str = format_duration(duration)

        # Extract metrics
        test_results = result.get("results", {}).get("tests", {})
        coverage_results = result.get("results", {}).get("coverage", {})
        security_results = result.get("results", {}).get("security", {})

        tests_total = test_results.get("total", 0)
        tests_passed = test_results.get("passed", 0)
        tests_str = f"{tests_passed}/{tests_total}" if tests_total > 0 else "-"

        coverage_percent = coverage_results.get("total_percent", 0)
        coverage_str = f"{coverage_percent}%" if coverage_percent > 0 else "-"

        findings_count = len(security_results.get("findings", []))
        severity_counts = security_results.get("severity_counts", {})
        errors = severity_counts.get("error", 0)
        warnings = severity_counts.get("warning", 0)
        critical = severity_counts.get("critical", 0)

        if findings_count > 0:
            # Show critical separately if present
            if critical > 0:
                security_str = f"{critical}C/{errors}E/{warnings}W"
            else:
                security_str = f"{errors}E/{warnings}W"
        else:
            security_str = "0 findings"

        md.append(f"| {job_name} | {status_icon} | {duration_str} | {tests_str} | {coverage_str} | {security_str} |")

    md.append("")

    # Details section
    md.append("## Details\n")

    if all_success:
        md.append("All checks passed! 🎉\n")
    else:
        md.append("Some checks failed. See details below:\n")

        for result in results:
            if result.get("status") != "success":
                job_name = result.get("job_name", "Unknown")
                md.append(f"### {job_name}\n")

                # Show test failures
                failures = result.get("results", {}).get("tests", {}).get("failures", [])
                if failures:
                    md.append("**Test Failures:**\n")
                    for failure in failures:
                        test_name = failure.get("test_name", "unknown")
                        error_msg = failure.get("error_message", "No error message")
                        md.append(f"- `{test_name}`")
                        md.append(f"  ```\n  {error_msg}\n  ```\n")

                # Show security findings
                findings = result.get("results", {}).get("security", {}).get("findings", [])
                if findings:
                    md.append("**Security Findings:**\n")
                    for finding in findings:
                        severity = finding.get("severity", "info").upper()
                        rule_id = finding.get("rule_id", "unknown")
                        file = finding.get("file", "unknown")
                        line = finding.get("line", 0)
                        message = finding.get("message", "No message")
                        md.append(f"- [{severity}] {rule_id} at {file}:{line}")
                        md.append(f"  {message}\n")

    return "\n".join(md)


def main():
    results_dir = Path("results")
    results = load_results(results_dir)

    summary = generate_summary(results)

    # Write to GitHub step summary
    github_step_summary = os.getenv("GITHUB_STEP_SUMMARY")
    if github_step_summary:
        with open(github_step_summary, "w") as f:
            f.write(summary)
        print("Summary written to GitHub step summary")
    else:
        print("GITHUB_STEP_SUMMARY not set, printing to stdout:")
        print(summary)


if __name__ == "__main__":
    main()
