# Automated Package Releases Design

**Date:** 2025-11-30
**Status:** ✅ Implemented
**Implementation:** See [2025-11-30-automated-package-releases.md](2025-11-30-automated-package-releases.md)

## Overview

Automated package building and publishing triggered by Uplift version tags. Packages are built using uv and published to both GitHub Packages (Python registry) and GitHub Releases with installation instructions.

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
   - Generates GitHub App token
   - Builds source distribution (.tar.gz)
   - Builds wheel (.whl)
   - Publishes to GitHub Packages registry
   - Creates GitHub Release
   - Attaches artifacts
   - Adds installation instructions
   ↓
10. Users install from GitHub Packages or download from GitHub Releases
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
- **Authentication:** GitHub App (APP_ID + PRIVATE_KEY)
- **Build Tool:** uv
- **Publishing:**
  - GitHub Packages registry: `https://pypi.pkg.github.com/jacaudi/`
  - GitHub Releases: Attachments with auto-generated notes
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

#### From GitHub Packages (Recommended)

```bash
# Using pipx (recommended for CLI tools)
pipx install ytdl-nfo --index-url https://pypi.pkg.github.com/jacaudi/simple/

# Using uv
uv tool install ytdl-nfo --index-url https://pypi.pkg.github.com/jacaudi/simple/

# Using pip
pip install ytdl-nfo --index-url https://pypi.pkg.github.com/jacaudi/simple/
```

**Note:** Authentication with GitHub personal access token may be required for private repositories.

#### From GitHub Releases

Download `.whl` file from releases and install directly:

```bash
pipx install ytdl_nfo-VERSION-py3-none-any.whl
uv tool install ytdl_nfo-VERSION-py3-none-any.whl
pip install ytdl_nfo-VERSION-py3-none-any.whl
```

### For Python Projects

#### From GitHub Packages

**With uv (pyproject.toml):**
```toml
[[tool.uv.index]]
name = "github-packages"
url = "https://pypi.pkg.github.com/jacaudi/simple/"

[project]
dependencies = ["ytdl-nfo"]
```

**With pip:**
```bash
pip config set global.index-url https://pypi.pkg.github.com/jacaudi/simple/
pip install ytdl-nfo
```

#### From GitHub Releases

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
- Contents: Read and write (push commits/tags, create releases)
- Packages: Write (publish to GitHub Packages)
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
- [x] Packages published to GitHub Packages registry
- [x] GitHub Releases created automatically
- [x] Installation instructions in release notes (both sources)
- [x] README updated with installation methods (both sources)
- [x] Local build verification passes
