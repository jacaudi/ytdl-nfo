# CI JSON Reporting Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add JSON-based result reporting where each CI job outputs structured data that a final Report job collects and presents as a unified GitHub job summary.

**Architecture:** Each job generates a standardized JSON artifact with test results, coverage, and security findings. A final Report job downloads all artifacts and renders a markdown summary to GitHub's job summary UI.

**Tech Stack:** Python 3 (stdlib only: json, pathlib), GitHub Actions (artifacts, job summary), pytest-json-report, coverage json, semgrep --json

---

## Task 1: Create Test Report Generator Script

**Files:**
- Create: `.github/scripts/generate-test-report.py`

**Step 1: Write the script structure**

Create `.github/scripts/generate-test-report.py`:

```python
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
```

**Step 2: Make script executable**

Run:
```bash
chmod +x .github/scripts/generate-test-report.py
```

**Step 3: Commit**

```bash
git add .github/scripts/generate-test-report.py
git commit -m "feat: add test report generator script

Generates standardized JSON reports from pytest and coverage output.
Handles missing files gracefully and extracts test results, coverage
metrics, and failure details into our standard schema."
```

---

## Task 2: Create Semgrep Report Generator Script

**Files:**
- Create: `.github/scripts/generate-semgrep-report.py`

**Step 1: Write the script**

Create `.github/scripts/generate-semgrep-report.py`:

```python
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
    severity_counts = {"error": 0, "warning": 0, "info": 0}

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
    status = "failure" if severity_counts["error"] > 0 else "success"

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
```

**Step 2: Make script executable**

Run:
```bash
chmod +x .github/scripts/generate-semgrep-report.py
```

**Step 3: Commit**

```bash
git add .github/scripts/generate-semgrep-report.py
git commit -m "feat: add semgrep report generator script

Generates standardized JSON reports from semgrep output.
Extracts findings, severity levels, and determines pass/fail status
based on error count."
```

---

## Task 3: Create Summary Generator Script

**Files:**
- Create: `.github/scripts/generate-summary.py`

**Step 1: Write the script**

Create `.github/scripts/generate-summary.py`:

```python
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

        if findings_count > 0:
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
```

**Step 2: Make script executable**

Run:
```bash
chmod +x .github/scripts/generate-summary.py
```

**Step 3: Commit**

```bash
git add .github/scripts/generate-summary.py
git commit -m "feat: add summary generator script

Generates unified GitHub job summary from all CI result JSONs.
Creates markdown table with status, metrics, and detailed failure info.
Handles missing results gracefully."
```

---

## Task 4: Update Code Validation Job

**Files:**
- Modify: `.github/workflows/ci.yml:15-29`

**Step 1: Update Code Validation job**

Modify `.github/workflows/ci.yml` test job to:

```yaml
  test:
    name: Code Validation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Run tests in devcontainer
        id: devcontainer
        uses: devcontainers/ci@v0.3.1900000417
        with:
          push: never
          runCmd: |
            uv sync --extra dev
            uv run ruff check ytdl_nfo
            START_TIME=$(date +%s)
            uv run pytest --json-report --json-report-file=pytest-report.json
            uv run coverage json
            END_TIME=$(date +%s)
            DURATION=$((END_TIME - START_TIME))
            python .github/scripts/generate-test-report.py "Code Validation" pytest-report.json coverage.json $DURATION

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: code-validation-results
          path: results.json
```

**Step 2: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "feat: add JSON reporting to Code Validation job

Modified job to generate pytest JSON report, coverage JSON, and create
standardized result JSON. Uploads results as artifact even on failure."
```

---

## Task 5: Update Security Scan Job

**Files:**
- Modify: `.github/workflows/ci.yml:31-44`

**Step 1: Update Security Scan job**

Modify `.github/workflows/ci.yml` semgrep job to:

```yaml
  semgrep:
    name: Security Scan
    runs-on: ubuntu-latest
    permissions:
      contents: read
    container:
      image: semgrep/semgrep:1.144.0
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Run Semgrep
        id: semgrep
        run: |
          START_TIME=$(date +%s)
          semgrep scan --config auto --json --output semgrep-report.json || true
          END_TIME=$(date +%s)
          DURATION=$((END_TIME - START_TIME))
          python3 .github/scripts/generate-semgrep-report.py "Security Scan" semgrep-report.json $DURATION

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: security-scan-results
          path: results.json
```

**Step 2: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "feat: add JSON reporting to Security Scan job

Modified job to generate semgrep JSON report and create standardized
result JSON. Uploads results as artifact even on failure."
```

---

## Task 6: Add Report Job

**Files:**
- Modify: `.github/workflows/ci.yml` (add new job after semgrep)

**Step 1: Add Report job**

Add this new job to `.github/workflows/ci.yml`:

```yaml
  report:
    name: Test Report
    runs-on: ubuntu-latest
    needs: [test, semgrep]
    if: always()
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: results/

      - name: Generate summary
        run: python .github/scripts/generate-summary.py
```

**Step 2: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "feat: add Report job to CI workflow

New job downloads all result artifacts and generates unified GitHub
job summary. Runs even if test jobs fail to show partial results."
```

---

## Task 7: Test the Implementation

**Step 1: Push branch and verify CI**

Run:
```bash
git push -u origin feature/ci-json-reporting
```

Expected: CI runs with all three jobs

**Step 2: Check GitHub Actions UI**

Navigate to: Repository → Actions → Latest workflow run

Verify:
- Code Validation job uploads artifact
- Security Scan job uploads artifact
- Report job shows summary in UI

**Step 3: Test failure scenario**

Create intentional test failure:
```bash
# In a test file, add: assert False, "Test failure scenario"
git commit -am "test: intentional failure to verify reporting"
git push
```

Verify:
- Report job still runs
- Summary shows failure details

**Step 4: Revert test failure**

```bash
git revert HEAD
git push
```

---

## Task 8: Update Design Document

**Files:**
- Modify: `docs/plans/2025-11-29-ci-json-reporting-design.md`

**Step 1: Add implementation status**

Update design doc header:
```markdown
**Date:** 2025-11-29
**Status:** ✅ Implemented
**Implementation:** See `docs/plans/2025-11-29-ci-json-reporting.md`
```

**Step 2: Commit**

```bash
git add docs/plans/2025-11-29-ci-json-reporting-design.md
git commit -m "docs: mark CI JSON reporting design as implemented"
```

---

## Verification Checklist

After completing all tasks:

- [ ] All three scripts are executable and in `.github/scripts/`
- [ ] Code Validation job generates and uploads JSON artifact
- [ ] Security Scan job generates and uploads JSON artifact
- [ ] Report job downloads artifacts and shows summary
- [ ] Summary displays correctly in GitHub Actions UI
- [ ] Failure scenarios show detailed error information
- [ ] All commits follow conventional commit format
- [ ] Design document updated with implementation status

---

## Notes

- Uses only Python stdlib (no external dependencies)
- Scripts handle missing files/data gracefully
- Jobs use `if: always()` to ensure reporting even on failure
- Artifacts are named uniquely to avoid conflicts
- Summary format is readable and actionable
