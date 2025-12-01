# Installation Guide

Complete installation instructions for ytdl-nfo across different platforms and package managers.

## Table of Contents

- [For End Users](#for-end-users)
  - [From GitHub Packages (Recommended)](#from-github-packages-recommended)
  - [From GitHub Releases](#from-github-releases)
- [For Python Projects](#for-python-projects)
  - [Using GitHub Packages](#using-github-packages)
  - [Using GitHub Releases](#using-github-releases)
- [Authentication](#authentication)

## For End Users

### From GitHub Packages (Recommended)

Install directly from the GitHub Packages registry:

```bash
# Using pipx (recommended for CLI tools)
pipx install ytdl-nfo --index-url https://pypi.pkg.github.com/jacaudi/simple/

# Using uv
uv tool install ytdl-nfo --index-url https://pypi.pkg.github.com/jacaudi/simple/

# Using pip
pip install ytdl-nfo --index-url https://pypi.pkg.github.com/jacaudi/simple/
```

**Note:** Authentication may be required. See [Authentication](#authentication) section below.

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

**Note:** Replace `VERSION` with the actual version number (e.g., `0.1.0`).

## For Python Projects

### Using GitHub Packages

#### With uv (pyproject.toml)

```toml
[[tool.uv.index]]
name = "github-packages"
url = "https://pypi.pkg.github.com/jacaudi/simple/"

[project]
dependencies = [
    "ytdl-nfo"
]
```

#### With pip

Configure pip to use GitHub Packages as the package index:

```bash
# Set globally
pip config set global.index-url https://pypi.pkg.github.com/jacaudi/simple/
pip install ytdl-nfo

# Or per-project (requirements.txt)
--index-url https://pypi.pkg.github.com/jacaudi/simple/
ytdl-nfo
```

#### With Poetry

```toml
[[tool.poetry.source]]
name = "github-packages"
url = "https://pypi.pkg.github.com/jacaudi/simple/"
priority = "primary"

[tool.poetry.dependencies]
ytdl-nfo = "*"
```

### Using GitHub Releases

#### With pip (requirements.txt)

```
ytdl-nfo @ https://github.com/jacaudi/ytdl-nfo/releases/download/vVERSION/ytdl_nfo-VERSION-py3-none-any.whl
```

#### With uv (pyproject.toml)

```toml
[project]
dependencies = [
    "ytdl-nfo @ https://github.com/jacaudi/ytdl-nfo/releases/download/vVERSION/ytdl_nfo-VERSION-py3-none-any.whl"
]
```

#### With Poetry

```bash
poetry add https://github.com/jacaudi/ytdl-nfo/releases/download/vVERSION/ytdl_nfo-VERSION-py3-none-any.whl
```

**Note:** Replace `VERSION` with the actual version number (e.g., `0.1.0`).

## Authentication

### GitHub Packages Authentication

To install packages from GitHub Packages, you may need to authenticate with a GitHub personal access token (PAT).

#### Creating a Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `read:packages` scope
3. Copy the token

#### Configuring Authentication

**With pip:**
```bash
# Add credentials to pip config
pip config set global.index-url https://USERNAME:TOKEN@pypi.pkg.github.com/jacaudi/simple/
```

**With uv:**
```bash
# Set environment variable
export UV_INDEX_URL=https://USERNAME:TOKEN@pypi.pkg.github.com/jacaudi/simple/
uv tool install ytdl-nfo
```

**With pipx:**
```bash
# Use environment variable
PIP_INDEX_URL=https://USERNAME:TOKEN@pypi.pkg.github.com/jacaudi/simple/ pipx install ytdl-nfo
```

**Note:** Replace `USERNAME` with your GitHub username and `TOKEN` with your personal access token.

### Security Note

**Never commit credentials to version control.** Use environment variables or secure credential storage:

```bash
# Store in environment variable
export GITHUB_TOKEN="your_token_here"
pip install ytdl-nfo --index-url https://USERNAME:${GITHUB_TOKEN}@pypi.pkg.github.com/jacaudi/simple/
```

## Verification

After installation, verify ytdl-nfo is installed correctly:

```bash
ytdl-nfo --help
```

You should see the help message with usage instructions.
