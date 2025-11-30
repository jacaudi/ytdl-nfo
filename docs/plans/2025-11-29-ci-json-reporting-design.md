# CI JSON Reporting System Design

**Date:** 2025-11-29
**Status:** ✅ Implemented
**Implementation:** See [2025-11-29-ci-json-reporting.md](2025-11-29-ci-json-reporting.md)

## Overview

Add JSON-based result reporting to CI workflow where each job outputs structured data that a final "Report" job collects and presents as a unified GitHub job summary.

## Requirements

- Each job outputs JSON with test results, coverage metrics, and security findings
- Final job presents unified summary via GitHub job summary (markdown)
- Report partial results if some jobs fail
- Standardized JSON schema for all jobs for easy extension

## Architecture

### Approach: Artifacts + Download

Jobs upload JSON as artifacts, final job downloads all and generates summary.

**Benefits:**
- Built-in GitHub feature, reliable
- Works on GitHub-hosted runners
- Simple implementation
- No size limits for our use case

## JSON Schema

Standard schema for all jobs:

```json
{
  "job_name": "Code Validation",
  "status": "success|failure|skipped",
  "duration_seconds": 42,
  "timestamp": "2025-11-29T21:30:00Z",
  "results": {
    "tests": {
      "total": 22,
      "passed": 22,
      "failed": 0,
      "skipped": 0,
      "failures": []  // Array of {test_name, error_message}
    },
    "coverage": {
      "total_percent": 76,
      "files": {
        "ytdl_nfo/nfo.py": {"percent": 87, "missing_lines": "37-39, 77"}
      }
    },
    "security": {
      "findings": [],  // For semgrep job
      "severity_counts": {"error": 0, "warning": 0, "info": 0}
    }
  }
}
```

## Data Flow

1. Each job (Code Validation, Security Scan) runs its tests/checks
2. Job captures output and converts to JSON using standard schema
3. Job uploads JSON as artifact named `<job-name>-results.json`
4. Final "Report" job (depends on all test jobs, uses `if: always()`) runs
5. Report job downloads all available artifacts
6. Report job parses JSONs and generates markdown summary
7. Report job writes summary using `$GITHUB_STEP_SUMMARY`

## Job Modifications

### Code Validation Job

1. Run tests as normal
2. Pytest outputs JSON via `--json-report` flag
3. Coverage outputs JSON via `coverage json`
4. Python script combines these into standard schema
5. Upload `results.json` as artifact

### Security Scan Job

1. Run semgrep with `--json` flag
2. Python script parses semgrep JSON into standard schema
3. Map semgrep severity to standard format
4. Upload `results.json` as artifact

### Implementation Details

- Small Python script per job: `.github/scripts/generate-*-report.py`
- Each job calls script with job-specific arguments
- Jobs use `continue-on-error: true` to upload JSON even on failure
- Upload artifact step uses `if: always()` to ensure upload happens

## Report Job

New job structure:

```yaml
report:
  name: Test Report
  runs-on: ubuntu-latest
  needs: [test, semgrep]
  if: always()  # Run even if test jobs fail
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

### Summary Generation

Script `.github/scripts/generate-summary.py`:
- Reads all JSON files from `results/` directory
- Handles missing files gracefully (job failed before upload)
- Generates markdown table with:
  - Job name, status (✓/✗), duration
  - Test results summary (22/22 passed)
  - Coverage percentage
  - Security findings count by severity
- Appends detailed sections for failures/findings
- Writes to `$GITHUB_STEP_SUMMARY`

**Example output:**

```markdown
# CI Results Summary

| Job | Status | Duration | Tests | Coverage | Security |
|-----|--------|----------|-------|----------|----------|
| Code Validation | ✓ | 28s | 22/22 | 76% | - |
| Security Scan | ✓ | 21s | - | - | 0 findings |

## Details
All checks passed! 🎉
```

### Error Handling

- Missing JSON = note job failed
- Malformed JSON = log warning, show "N/A"
- Empty results directory = show "No results available"

## File Structure

```
.github/
  workflows/
    ci.yml                          # Modified jobs + new report job
  scripts/
    generate-test-report.py         # Code Validation → JSON
    generate-semgrep-report.py      # Security Scan → JSON
    generate-summary.py             # Report job
```

## Testing Strategy

1. Add report generation to a test branch first
2. Intentionally break a test to verify failure reporting
3. Verify JSON schema is correct and parseable
4. Confirm summary renders properly in GitHub UI
5. Test with missing artifacts (simulate job failure)

## Rollout Plan

- **Phase 1:** Add JSON generation to existing jobs (non-breaking)
- **Phase 2:** Add report job (observe, don't rely on it yet)
- **Phase 3:** Iterate on summary format based on real usage
- **Phase 4:** Consider adding trend tracking later (optional)

## Future Extensibility

With standard schema, easy to add:
- New jobs (just follow schema, upload artifact)
- Historical trend tracking (compare with previous runs)
- Threshold enforcement (fail if coverage drops)
- Slack/Discord notifications (parse JSON, send webhook)

## Dependencies

- Python 3 (already available in ubuntu-latest)
- No external packages needed (use stdlib: json, pathlib)
- `actions/download-artifact@v4`

## Success Criteria

- [x] All CI jobs produce valid JSON artifacts
- [x] Report job successfully downloads and parses artifacts
- [x] GitHub job summary displays correctly
- [x] Partial results shown when jobs fail
- [x] Easy to add new jobs following the same pattern
