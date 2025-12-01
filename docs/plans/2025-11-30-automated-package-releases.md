# Automated Package Releases Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement automated package building and GitHub Release creation triggered by Uplift version tags, with installation instructions for users.

**Architecture:** Tag-based release workflow that builds Python packages (source distribution and wheel) and publishes them to GitHub Releases with auto-generated release notes and installation instructions. Uses GitHub App bot for authentication instead of PAT.

**Tech Stack:**
- Uplift for semantic versioning and tag creation
- GitHub Actions for automation
- uv for package building
- GitHub App for authenticated git operations
- softprops/action-gh-release for release creation

---

## Task 1: Create Uplift Configuration

**Files:**
- Create: `.uplift.yml`

**Step 1: Create Uplift configuration file**

Create `.uplift.yml` in project root:

```yaml
# Uplift configuration for semantic versioning and changelog generation
git:
  ignoreDetached: false

bumps:
  # Update pyproject.toml version field
  - file: pyproject.toml
    regex:
      - pattern: 'version = "([0-9]+\.[0-9]+\.[0-9]+)"'
        semver: true
        count: 1

changelog:
  sort: asc
  exclude:
    - ^chore
    - ^ci
    - ^docs
    - ^style
    - ^test
```

**Step 2: Verify configuration syntax**

Run: `cat .uplift.yml`
Expected: File contents display correctly with proper YAML syntax

**Step 3: Commit**

```bash
git add .uplift.yml
git commit -m "feat: add Uplift configuration for semantic versioning

Configures Uplift to:
- Bump version in pyproject.toml
- Generate changelog excluding chore/ci/docs/style/test commits
- Use semantic versioning (v1.2.3 format)"
```

---

## Task 2: Rename and Update Uplift Workflow

**Files:**
- Rename: `.github/workflows/uplfitci.yaml` → `.github/workflows/uplift.yaml`
- Modify: `.github/workflows/uplift.yaml` (lines 1-41, entire file)

**Step 1: Rename workflow file**

Run: `git mv .github/workflows/uplfitci.yaml .github/workflows/uplift.yaml`
Expected: File renamed successfully

**Step 2: Update workflow to use GitHub App authentication**

Replace entire contents of `.github/workflows/uplift.yaml`:

```yaml
name: Release

on:
  workflow_dispatch:

permissions:
  contents: write
  packages: write

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Check authorization
        if: github.actor != github.repository_owner
        run: |
          echo "Only the repository owner can trigger releases"
          echo "Actor: ${{ github.actor }}"
          echo "Owner: ${{ github.repository_owner }}"
          exit 1

      - name: Checkout
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Generate GitHub App Token
        id: app-token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.PRIVATE_KEY }}

      - name: Configure git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Run Uplift
        uses: gembaadvantage/uplift-action@v2.0.2
        with:
          args: release
        env:
          GITHUB_TOKEN: ${{ steps.app-token.outputs.token }}
```

**Step 3: Verify workflow syntax**

Run: `cat .github/workflows/uplift.yaml`
Expected: Valid YAML with GitHub App token generation step

**Step 4: Commit**

```bash
git add .github/workflows/uplift.yaml
git commit -m "refactor: rename uplift workflow and use GitHub App auth

- Renamed uplfitci.yaml to uplift.yaml for clarity
- Replaced PAT_TOKEN with GitHub App authentication
- Uses APP_ID and PRIVATE_KEY secrets for token generation"
```

---

## Task 3: Create Release Workflow

**Files:**
- Create: `.github/workflows/release.yaml`

**Step 1: Create release workflow file**

Create `.github/workflows/release.yaml`:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*.*.*'  # Trigger on version tags (v1.2.3)

permissions:
  contents: write  # Required to create releases

jobs:
  build-and-release:
    name: Build and Release Package
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Build package
        run: uv build

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: |
            dist/*.tar.gz
            dist/*.whl
          body: |
            ## Installation from GitHub Release

            Download the `.whl` file from the assets below, then:

            ### Using pipx (recommended for CLI tools)
            ```bash
            pipx install ytdl_nfo-${{ github.ref_name }}-py3-none-any.whl
            ```

            ### Using uv
            ```bash
            uv tool install ytdl_nfo-${{ github.ref_name }}-py3-none-any.whl
            ```

            ### Using pip
            ```bash
            pip install ytdl_nfo-${{ github.ref_name }}-py3-none-any.whl
            ```
          generate_release_notes: true
          draft: false
```

**Step 2: Verify workflow syntax**

Run: `cat .github/workflows/release.yaml`
Expected: Valid YAML with tag trigger and release steps

**Step 3: Commit**

```bash
git add .github/workflows/release.yaml
git commit -m "feat: add automated release workflow

Workflow triggers on version tags created by Uplift:
- Builds source distribution and wheel using uv
- Creates GitHub Release with installation instructions
- Attaches built packages as release assets
- Generates release notes from commits"
```

---

## Task 4: Update README with Installation Instructions

**Files:**
- Modify: `README.md` (after existing installation section)

**Step 1: Read current README to find installation section**

Run: `grep -n "## " README.md | head -20`
Expected: Shows section headings and line numbers

**Step 2: Add new installation section**

Add after the existing usage/installation content in README.md:

```markdown
## Installation

### From GitHub Releases

Download the latest `.whl` file from [Releases](https://github.com/jacaudi/ytdl-nfo/releases), then:

```bash
# Using pipx (recommended for CLI tools)
pipx install ytdl_nfo-VERSION-py3-none-any.whl

# Using uv
uv tool install ytdl_nfo-VERSION-py3-none-any.whl

# Using pip
pip install ytdl_nfo-VERSION-py3-none-any.whl
```

### Using in Python Projects

To use ytdl-nfo packages from GitHub Releases in your Python projects:

**With pip (requirements.txt):**
```
ytdl-nfo @ https://github.com/jacaudi/ytdl-nfo/releases/download/vVERSION/ytdl_nfo-VERSION-py3-none-any.whl
```

**With uv (pyproject.toml):**
```toml
[project]
dependencies = [
    "ytdl-nfo @ https://github.com/jacaudi/ytdl-nfo/releases/download/vVERSION/ytdl_nfo-VERSION-py3-none-any.whl"
]
```

**With Poetry:**
```bash
poetry add https://github.com/jacaudi/ytdl-nfo/releases/download/vVERSION/ytdl_nfo-VERSION-py3-none-any.whl
```
```

**Note:** Replace `VERSION` with the actual version number (e.g., `0.1.0`).

**Step 3: Verify README formatting**

Run: `head -100 README.md`
Expected: New installation section appears with proper markdown formatting

**Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add installation instructions for GitHub Releases

Added instructions for:
- Installing from GitHub Releases using pipx/uv/pip
- Using packages in Python projects (requirements.txt, pyproject.toml, Poetry)
- Direct download and installation from release assets"
```

---

## Task 5: Test Package Build Locally

**Files:**
- None (verification task)

**Step 1: Build package with uv**

Run: `uv build`
Expected:
```
Building ytdl-nfo @ file:///path/to/ytdl-nfo
Built ytdl-nfo @ file:///path/to/ytdl-nfo
```

**Step 2: Verify build artifacts**

Run: `ls -lh dist/`
Expected: Two files created:
- `ytdl_nfo-X.Y.Z.tar.gz` (source distribution)
- `ytdl_nfo-X.Y.Z-py3-none-any.whl` (wheel)

**Step 3: Inspect wheel contents**

Run: `unzip -l dist/ytdl_nfo-*.whl | head -20`
Expected: Shows wheel contents including:
- ytdl_nfo/ directory
- ytdl_nfo-X.Y.Z.dist-info/ directory
- Python files (.py)
- Config files (.yaml)

**Step 4: Clean build artifacts**

Run: `rm -rf dist/`
Expected: dist/ directory removed

**Step 5: Document build verification**

No commit needed - this is a verification step.

---

## Task 6: Create Design Documentation

**Files:**
- Create: `docs/plans/2025-11-30-automated-package-releases-design.md`

**Step 1: Create design document**

Create `docs/plans/2025-11-30-automated-package-releases-design.md`:

```markdown
# Automated Package Releases Design

**Date:** 2025-11-30
**Status:** ✅ Implemented
**Implementation:** See [2025-11-30-automated-package-releases.md](2025-11-30-automated-package-releases.md)

## Overview

Automated package building and GitHub Release creation triggered by Uplift version tags. Packages are built using uv and published to GitHub Releases with installation instructions.

## Architecture

### Release Flow

```
1. Developer commits with conventional commit message
   ↓
2. Merge to main (via PR or direct push)
   ↓
3. Manual trigger of Uplift workflow (workflow_dispatch)
   ↓
4. Uplift analyzes commits since last tag
   ↓
5. Uplift bumps version in pyproject.toml
   ↓
6. Uplift creates git tag (v1.2.3)
   ↓
7. Uplift pushes tag to remote
   ↓
8. Tag push triggers Release workflow
   ↓
9. Release workflow:
   - Builds source distribution (.tar.gz)
   - Builds wheel (.whl)
   - Creates GitHub Release
   - Attaches artifacts
   - Adds installation instructions
   ↓
10. Users download from GitHub Releases
```

### Components

#### Uplift Configuration (.uplift.yml)

- **Purpose:** Define version bumping rules and changelog generation
- **Version Source:** `pyproject.toml` version field
- **Tag Format:** `v{major}.{minor}.{patch}` (e.g., v0.1.0)
- **Changelog:** Excludes chore, ci, docs, style, test commits

#### Uplift Workflow (.github/workflows/uplift.yaml)

- **Trigger:** Manual (workflow_dispatch)
- **Requirements:**
  - Only runs on main branch
  - Only repository owner can trigger
- **Authentication:** GitHub App (APP_ID + PRIVATE_KEY)
- **Actions:**
  - Generates short-lived token from GitHub App
  - Runs Uplift to bump version and create tag
  - Pushes tag to remote

#### Release Workflow (.github/workflows/release.yaml)

- **Trigger:** Tag push (v*.*.*)
- **Build Tool:** uv
- **Artifacts:**
  - Source distribution: `ytdl_nfo-{version}.tar.gz`
  - Wheel: `ytdl_nfo-{version}-py3-none-any.whl`
- **Release Notes:** Auto-generated from commits + installation instructions

## Conventional Commit → Version Bump

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | Minor (0.1.0 → 0.2.0) | New feature |
| `fix:` | Patch (0.1.0 → 0.1.1) | Bug fix |
| `feat!:` or `BREAKING CHANGE:` | Major (0.1.0 → 1.0.0) | Breaking change |
| `chore:`, `docs:`, `style:`, `test:` | None | No version bump |

## Installation Methods

### For End Users

1. **pipx** (recommended for CLI tools)
2. **uv tool install**
3. **pip install**

### For Python Projects

- **pip:** requirements.txt with GitHub URL
- **uv:** pyproject.toml dependencies with GitHub URL
- **Poetry:** poetry add with GitHub URL

## Future: PyPI Publishing

To add PyPI publishing later:

1. Create PyPI account and generate API token
2. Add `PYPI_TOKEN` to GitHub secrets
3. Add publish step to release workflow:
```yaml
- name: Publish to PyPI
  run: uv publish
  env:
    UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
```
4. Optionally test with Test PyPI first

## Authentication: GitHub App vs PAT

**Chosen Approach:** GitHub App

**Benefits:**
- Scoped to specific repositories
- More granular permissions
- Better audit trail (shows as bot, not user)
- Token auto-expires (more secure)
- Doesn't count against user rate limits

**Required Permissions:**
- Contents: Read and write (push commits/tags)
- Metadata: Read (default)

**Required Secrets:**
- `APP_ID`: GitHub App ID (numeric)
- `PRIVATE_KEY`: GitHub App private key (.pem file)

## Files Modified/Created

### Created:
- `.uplift.yml` - Uplift configuration
- `.github/workflows/release.yaml` - Release automation

### Modified:
- `.github/workflows/uplfitci.yaml` → `.github/workflows/uplift.yaml` - Renamed and updated
- `README.md` - Added installation instructions

## Testing Strategy

### Local Testing:
1. `uv build` - Verify package builds
2. `ls dist/` - Check artifacts created
3. `unzip -l dist/*.whl` - Inspect wheel contents

### CI Testing:
1. Create test tag manually: `git tag v0.0.1-test && git push origin v0.0.1-test`
2. Verify release workflow triggers
3. Verify artifacts attached to release
4. Verify installation instructions in release notes
5. Delete test release and tag

### End-to-End Testing:
1. Make a conventional commit (e.g., `feat: test release`)
2. Merge to main
3. Trigger Uplift workflow
4. Verify tag created
5. Verify release created automatically
6. Download and test installation with pipx/uv/pip

## Success Criteria

- [x] Uplift configuration created
- [x] Uplift workflow uses GitHub App authentication
- [x] Release workflow triggers on version tags
- [x] Packages build successfully (source + wheel)
- [x] GitHub Releases created automatically
- [x] Installation instructions in release notes
- [x] README updated with installation methods
- [x] Local build verification passes
```

**Step 2: Verify design document**

Run: `wc -l docs/plans/2025-11-30-automated-package-releases-design.md`
Expected: Document created with substantial content

**Step 3: Commit**

```bash
git add docs/plans/2025-11-30-automated-package-releases-design.md
git commit -m "docs: add automated package releases design document

Comprehensive design documentation covering:
- Architecture and release flow
- Component descriptions
- Conventional commit versioning rules
- Installation methods
- Future PyPI publishing approach
- GitHub App authentication benefits
- Testing strategy"
```

---

## Task 7: Verify GitHub Secrets Configuration

**Files:**
- None (verification task)

**Step 1: Check that required secrets exist**

Run: `gh secret list`
Expected output should include:
```
APP_ID          Updated YYYY-MM-DD
PRIVATE_KEY     Updated YYYY-MM-DD
```

**Step 2: If secrets missing, guide user**

If `APP_ID` or `PRIVATE_KEY` are not in the list, output:

```
REQUIRED: GitHub App secrets are not configured.

To configure:
1. Go to repository Settings → Secrets and variables → Actions
2. Add secret: APP_ID (your GitHub App ID number)
3. Add secret: PRIVATE_KEY (your GitHub App .pem file contents)

Then re-run this verification step.
```

**Step 3: Document verification**

No commit needed - this is a verification step.

---

## Verification and Testing

After all tasks complete:

### Local Verification:
```bash
# 1. Verify all files created/modified
git status

# 2. Verify package builds
uv build
ls -lh dist/

# 3. Clean up
rm -rf dist/
```

### CI Verification (after pushing):
```bash
# 1. Push all commits
git push origin main

# 2. Trigger Uplift workflow manually via GitHub UI
# Go to Actions → Release → Run workflow

# 3. Monitor workflow execution
gh run watch

# 4. Verify tag created
git fetch --tags
git tag -l

# 5. Verify release created
gh release list

# 6. View release details
gh release view <tag>
```

### End-to-End Test:
```bash
# 1. Download release artifact
gh release download <tag> --pattern "*.whl"

# 2. Test installation
pipx install ytdl_nfo-*.whl --force

# 3. Verify installation
ytdl-nfo --version

# 4. Cleanup
pipx uninstall ytdl-nfo
rm ytdl_nfo-*.whl
```

---

## Rollout Plan

1. **Phase 1:** Implement all tasks (this plan)
2. **Phase 2:** Test with first release (v0.1.0 or similar)
3. **Phase 3:** Monitor release process for issues
4. **Phase 4:** Document any adjustments needed
5. **Future:** Add PyPI publishing when ready

---

## Notes

- Replace `VERSION` placeholders in README with actual version numbers
- Uplift workflow requires manual trigger (workflow_dispatch)
- Release workflow automatically triggers on tag push
- GitHub App provides better security than PAT
- Packages are Python 3-only (py3-none-any wheel)
- Source distribution and wheel both included
- Release notes auto-generated from commits

