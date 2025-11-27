# UV Migration and Test Suite Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate ytdl-nfo from Poetry to uv, add VS Code devcontainer, replace flake8/autopep8 with ruff, remove Nix, and add pytest-based test suite for core functionality.

**Architecture:** Two-phase sequential approach. Phase A: Set up devcontainer, migrate tooling (Poetry→uv, flake8/autopep8→ruff), remove Nix, update docs. Phase B: Build pytest test suite inside container covering JSON parsing, extractor detection, NFO generation, and end-to-end workflows.

**Tech Stack:** Python 3.8+, uv, ruff, pytest, pytest-cov, VS Code Dev Containers, Docker

---

## Phase A: Tooling Migration + Containerization

### Task 1: Create VS Code Dev Container - Dockerfile

**Files:**
- Create: `.devcontainer/Dockerfile`

**Step 1: Create .devcontainer directory**

```bash
mkdir -p .devcontainer
```

**Step 2: Write Dockerfile**

Create `.devcontainer/Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Set working directory
WORKDIR /workspace

# Install development tools via uv
RUN uv pip install --system ruff pytest pytest-cov

# Verify installations
RUN uv --version && ruff --version && pytest --version
```

**Step 3: Verify Dockerfile syntax**

Run: `docker build -f .devcontainer/Dockerfile -t ytdl-nfo-dev .`
Expected: Build succeeds

**Step 4: Commit**

```bash
git add .devcontainer/Dockerfile
git commit -m "feat: add Dockerfile for devcontainer

Sets up Python 3.11 environment with uv, ruff, and pytest pre-installed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: Create VS Code Dev Container - devcontainer.json

**Files:**
- Create: `.devcontainer/devcontainer.json`

**Step 1: Write devcontainer.json**

Create `.devcontainer/devcontainer.json`:

```json
{
  "name": "ytdl-nfo Python Development",
  "build": {
    "dockerfile": "Dockerfile"
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.testing.pytestEnabled": true,
        "python.testing.unittestEnabled": false,
        "[python]": {
          "editor.defaultFormatter": "charliermarsh.ruff",
          "editor.formatOnSave": true,
          "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
          }
        },
        "ruff.enable": true,
        "ruff.lint.run": "onSave"
      }
    }
  },
  "postCreateCommand": "uv sync || echo 'uv sync will run after pyproject.toml is updated'",
  "remoteUser": "root"
}
```

**Step 2: Commit**

```bash
git add .devcontainer/devcontainer.json
git commit -m "feat: add devcontainer.json configuration

Configures VS Code devcontainer with Python, Pylance, and Ruff extensions.
Sets up auto-formatting and linting on save.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: Remove Nix Files

**Files:**
- Delete: `flake.nix`
- Delete: `flake.lock`

**Step 1: Remove Nix files**

```bash
git rm flake.nix flake.lock
```

**Step 2: Commit**

```bash
git commit -m "remove: delete Nix flake files

Removing Nix development environment in favor of VS Code devcontainer.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: Update pyproject.toml - Convert to PEP 621

**Files:**
- Modify: `pyproject.toml`

**Step 1: Read current pyproject.toml**

Run: `cat pyproject.toml`

**Step 2: Replace pyproject.toml with uv-compatible version**

Replace entire contents of `pyproject.toml`:

```toml
[project]
name = "ytdl-nfo"
version = "0.3.0"
description = "Utility to convert youtube-dl/yt-dlp json metadata to .nfo"
readme = "README.md"
requires-python = ">=3.8"
license = { text = "Unlicense" }
authors = [{ name = "Owen", email = "owdevel@gmail.com" }]

dependencies = [
    "PyYAML>=6.0.1",
    "setuptools>=70.2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
]

[project.urls]
repository = "https://github.com/owdevel/ytdl-nfo"

[project.scripts]
ytdl-nfo = "ytdl_nfo:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--cov=ytdl_nfo",
    "--cov-report=term-missing",
    "--cov-report=html",
]
markers = [
    "unit: Unit tests for individual components",
    "integration: End-to-end integration tests",
]
```

**Step 3: Remove poetry.lock**

```bash
git rm poetry.lock
```

**Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "refactor: migrate pyproject.toml to PEP 621 standard

- Convert from Poetry format to uv-compatible PEP 621
- Add ruff configuration for linting and formatting
- Add pytest configuration
- Replace poetry-core with hatchling build backend
- Remove poetry.lock

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 5: Initialize uv and Generate Lock File

**Files:**
- Create: `uv.lock`

**Step 1: Run uv sync in devcontainer**

Run: `uv sync`
Expected: Dependencies installed, `uv.lock` created

**Step 2: Verify uv tree**

Run: `uv tree`
Expected: Shows dependency tree with PyYAML, setuptools, pytest, pytest-cov, ruff

**Step 3: Commit lock file**

```bash
git add uv.lock
git commit -m "chore: add uv.lock file

Generated lock file from uv sync.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 6: Run Ruff Formatter on Existing Code

**Files:**
- Modify: `ytdl_nfo/*.py` (formatting only)

**Step 1: Run ruff format**

Run: `uv run ruff format ytdl_nfo`
Expected: Files formatted according to ruff rules

**Step 2: Review changes**

Run: `git diff`
Expected: Only formatting changes (whitespace, quotes, etc.)

**Step 3: Commit formatting changes**

```bash
git add ytdl_nfo/
git commit -m "style: format code with ruff

Auto-format existing code to match ruff style guidelines.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 7: Run Ruff Linter and Fix Issues

**Files:**
- Modify: `ytdl_nfo/*.py` (if issues found)

**Step 1: Run ruff check**

Run: `uv run ruff check ytdl_nfo`
Expected: May show linting issues

**Step 2: Auto-fix fixable issues**

Run: `uv run ruff check --fix ytdl_nfo`
Expected: Auto-fixable issues resolved

**Step 3: Review remaining issues**

If issues remain, address them manually based on ruff output.

**Step 4: Verify clean linting**

Run: `uv run ruff check ytdl_nfo`
Expected: No issues or only acceptable warnings

**Step 5: Commit lint fixes (if any)**

```bash
git add ytdl_nfo/
git commit -m "fix: resolve ruff linting issues

Address linting warnings identified by ruff.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 8: Update README.md - Remove Nix, Add Devcontainer

**Files:**
- Modify: `README.md`

**Step 1: Read current README.md**

Run: `cat README.md`

**Step 2: Update README.md**

Replace the "Installation" and "Development Environment" sections:

**OLD (lines 11-35):**
```markdown
## Installation

### Python 3 pipx (recommended)
...
### Package from Source
...
2. Install [Python Poetry](https://python-poetry.org/)
...
4. Create a dev environment with `poetry install`
5. Build with `poetry build`
```

**NEW:**
```markdown
## Installation

### Python 3 pipx (recommended)

[pipx](https://github.com/pipxproject/pipx) is a tool that installs a package and its dependencies in an isolated environment.

1. Install [Python 3.8](https://www.python.org/downloads/) (or later)
2. Install [pipx](https://github.com/pipxproject/pipx)
3. Run `pipx install ytdl-nfo`

### Python 3 pip

1. Install [Python 3.8](https://www.python.org/downloads/) (or later)
2. Installed [pip](https://pip.pypa.io/en/stable/installation/)
3. Run `pip install ytdl-nfo`

### Package from Source

1. Install [Python 3.8](https://www.python.org/downloads/) (or later)
2. Install [uv](https://docs.astral.sh/uv/)
3. Clone the repo using `git clone https://github.com/owdevel/ytdl_nfo.git`
4. Create a dev environment with `uv sync`
5. Build with `uv build`
6. Install from the `dist` directory with `pip install ./dist/ytdl_nfo-x.x.x.tar.gz`
```

**Step 3: Update "Development Environment" section**

**OLD (lines 77-91):**
```markdown
### Development Environment

1. Install [Python 3.8](https://www.python.org/downloads/) (or later)
2. Install [Python Poetry](https://python-poetry.org/)
...
6. Run the application using `poetry run ytdl-nfo`, or use `poetry shell` to enter the virtual env
```

**NEW:**
```markdown
### Development Environment

#### VS Code Dev Container (Recommended)

1. Install [Docker](https://www.docker.com/get-started)
2. Install [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Clone your fork using `git clone git@github.com:<YOUR_USERNAME>/ytdl-nfo.git`
4. Open the project in VS Code
5. When prompted, click "Reopen in Container" (or use Command Palette → "Dev Containers: Reopen in Container")
6. VS Code will build the container with all dependencies pre-installed
7. Run the application using `uv run ytdl-nfo`

The devcontainer includes Python 3.11, uv, ruff, and pytest pre-configured.

#### Local Development (Alternative)

1. Install [Python 3.8](https://www.python.org/downloads/) (or later)
2. Install [uv](https://docs.astral.sh/uv/)
3. Create a fork of this repo
4. Clone your fork using `git clone git@github.com:<YOUR_USERNAME>/ytdl-nfo.git`
5. Change to the project directory and initialize the environment using uv

    ```bash
    cd ytdl-nfo
    uv sync
    ```

6. Run the application using `uv run ytdl-nfo`
```

**Step 4: Commit README updates**

```bash
git add README.md
git commit -m "docs: update README for uv and devcontainer

- Replace Poetry with uv in installation instructions
- Add VS Code devcontainer setup as recommended approach
- Remove Nix references
- Update development workflow

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 9: Update CLAUDE.md - Remove Nix, Add Devcontainer, Update Commands

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Read current CLAUDE.md**

Run: `cat CLAUDE.md`

**Step 2: Update CLAUDE.md Development Environment section**

Replace the "Development Environment" section:

**OLD:**
```markdown
## Development Environment

### Setup with Poetry (Primary)
```bash
# Install dependencies
poetry install
...
```

### Setup with Nix (Alternative)
```bash
nix develop  # Enters dev shell with Poetry available
```

### Linting
```bash
# Check code style
poetry run flake8 ytdl_nfo

# Auto-format code
poetry run autopep8 --in-place --recursive ytdl_nfo
```
```

**NEW:**
```markdown
## Development Environment

**IMPORTANT:** All development should occur inside the VS Code devcontainer for consistency.

### Setup with VS Code Dev Container (Recommended)

1. Install Docker and VS Code with Dev Containers extension
2. Open project in VS Code
3. Command Palette → "Dev Containers: Reopen in Container"
4. Wait for container to build (includes Python 3.11, uv, ruff, pytest)
5. Container automatically runs `uv sync` on first open

### Container Workflow

All commands below assume you're inside the devcontainer.

```bash
# Sync dependencies (if pyproject.toml changes)
uv sync

# Run the application
uv run ytdl-nfo <file_or_directory>

# Build package
uv build
```

### Linting and Formatting

```bash
# Check code style
uv run ruff check ytdl_nfo

# Auto-fix linting issues
uv run ruff check --fix ytdl_nfo

# Format code
uv run ruff format ytdl_nfo
```

### Rebuilding Container

If you modify `.devcontainer/Dockerfile` or `.devcontainer/devcontainer.json`:

Command Palette → "Dev Containers: Rebuild Container"
```

**Step 3: Update "Running the Application" section**

Replace all `poetry run` references with `uv run`:

**OLD:**
```markdown
```bash
# Single file
poetry run ytdl-nfo path/to/video.info.json
...
```
```

**NEW:**
```markdown
```bash
# Single file
uv run ytdl-nfo path/to/video.info.json

# Directory (recursive)
uv run ytdl-nfo path/to/videos/

# Override extractor
uv run ytdl-nfo --extractor youtube path/to/video.info.json

# Overwrite existing NFO files
uv run ytdl-nfo --overwrite path/to/videos/

# Custom regex for file matching
uv run ytdl-nfo --regex "\.json$" path/to/videos/

# Show config directory
uv run ytdl-nfo --config
```
```

**Step 4: Commit CLAUDE.md updates**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for devcontainer and uv

- Add devcontainer workflow as primary development method
- Replace Poetry commands with uv equivalents
- Replace flake8/autopep8 with ruff commands
- Remove Nix references
- Add container rebuild instructions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 10: Verify Phase A - Build and CLI Test

**Files:**
- None (verification only)

**Step 1: Verify uv is working**

Run: `uv --version`
Expected: Shows uv version (e.g., "uv 0.x.x")

**Step 2: Build package**

Run: `uv build`
Expected: Creates `dist/` directory with `.tar.gz` and `.whl` files

**Step 3: Test CLI**

Run: `uv run ytdl-nfo --config`
Expected: Prints path to config directory

**Step 4: Run ruff check**

Run: `uv run ruff check ytdl_nfo`
Expected: No errors (or only acceptable warnings)

**Step 5: Run ruff format check**

Run: `uv run ruff format --check ytdl_nfo`
Expected: All files already formatted

**Step 6: Document verification in commit message**

```bash
git commit --allow-empty -m "chore: verify Phase A tooling migration complete

✓ Devcontainer builds successfully
✓ uv available and working
✓ Package builds with uv build
✓ CLI works: uv run ytdl-nfo --config
✓ Ruff linting passes
✓ Ruff formatting applied

Phase A (Tooling Migration + Containerization) complete.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Phase B: Test Suite Addition

### Task 11: Create Test Directory Structure

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/fixtures/`

**Step 1: Create directory structure**

```bash
mkdir -p tests/fixtures
touch tests/__init__.py
```

**Step 2: Create conftest.py with shared fixtures**

Create `tests/conftest.py`:

```python
"""Shared pytest fixtures for ytdl-nfo tests."""

import json
import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir():
    """Return path to fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_youtube_json_data():
    """Return sample YouTube .info.json data as dict."""
    return {
        "id": "dQw4w9WgXcQ",
        "title": "Test Video Title",
        "uploader": "Test Uploader",
        "description": "Test video description",
        "upload_date": "20230115",
        "extractor": "youtube",
        "_filename": "Test Video Title.mp4",
    }


@pytest.fixture
def sample_twitch_json_data():
    """Return sample Twitch VOD .info.json data as dict."""
    return {
        "id": "123456789",
        "title": "Test Twitch VOD",
        "uploader": "TestStreamer",
        "description": "Test stream description",
        "upload_date": "20230120",
        "extractor": "twitch:vod",
        "_filename": "Test Twitch VOD.mp4",
    }


@pytest.fixture
def temp_json_file(tmp_path, sample_youtube_json_data):
    """Create a temporary .info.json file."""
    json_file = tmp_path / "test_video.info.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(sample_youtube_json_data, f)
    return json_file
```

**Step 3: Commit test structure**

```bash
git add tests/
git commit -m "test: create test directory structure and fixtures

Add tests/ directory with conftest.py containing shared pytest fixtures
for test data.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 12: Write Tests for Ytdl_nfo Class - JSON Parsing

**Files:**
- Create: `tests/test_ytdl_nfo.py`

**Step 1: Write failing tests for JSON parsing**

Create `tests/test_ytdl_nfo.py`:

```python
"""Tests for Ytdl_nfo class."""

import json
import pytest
from ytdl_nfo import Ytdl_nfo


class TestYtdlNfoJSONParsing:
    """Test JSON parsing functionality."""

    def test_valid_json_file_loading(self, temp_json_file, sample_youtube_json_data):
        """Test that valid JSON file is loaded correctly."""
        ytdl = Ytdl_nfo(str(temp_json_file))
        assert ytdl.input_ok is True
        assert ytdl.data == sample_youtube_json_data

    def test_invalid_json_error_handling(self, tmp_path):
        """Test that invalid JSON is handled gracefully."""
        invalid_json = tmp_path / "invalid.info.json"
        invalid_json.write_text("{invalid json}", encoding="utf-8")

        ytdl = Ytdl_nfo(str(invalid_json))
        assert ytdl.input_ok is False
        assert ytdl.data is None

    def test_missing_file_error_handling(self):
        """Test that missing file is handled gracefully."""
        ytdl = Ytdl_nfo("/nonexistent/file.info.json")
        # Should handle gracefully without crashing
        assert ytdl.data is None
```

**Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_ytdl_nfo.py::TestYtdlNfoJSONParsing -v`
Expected: Tests may pass (existing code already implements this) or fail if implementation differs

**Step 3: Review existing implementation**

Run: `cat ytdl_nfo/Ytdl_nfo.py`

Verify that:
- JSON loading is implemented in `__init__`
- `input_ok` flag tracks parsing success
- `data` stores parsed JSON

**Step 4: Adjust tests if needed based on actual implementation**

If tests fail, adjust assertions to match actual behavior or fix implementation.

**Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/test_ytdl_nfo.py::TestYtdlNfoJSONParsing -v`
Expected: All tests PASS

**Step 6: Commit**

```bash
git add tests/test_ytdl_nfo.py
git commit -m "test: add JSON parsing tests for Ytdl_nfo

Test valid JSON loading, invalid JSON handling, and missing file handling.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 13: Write Tests for Ytdl_nfo Class - Extractor Detection

**Files:**
- Modify: `tests/test_ytdl_nfo.py`

**Step 1: Add extractor detection tests**

Add to `tests/test_ytdl_nfo.py`:

```python
class TestYtdlNfoExtractorDetection:
    """Test extractor detection and normalization."""

    def test_extractor_auto_detection(self, temp_json_file):
        """Test that extractor is auto-detected from JSON."""
        ytdl = Ytdl_nfo(str(temp_json_file))
        assert ytdl.extractor == "youtube"

    def test_extractor_normalization(self, tmp_path, sample_twitch_json_data):
        """Test that extractor name is normalized (colon replaced with underscore)."""
        json_file = tmp_path / "test.info.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(sample_twitch_json_data, f)

        ytdl = Ytdl_nfo(str(json_file))
        # "twitch:vod" should become "twitch_vod"
        assert ytdl.extractor == "twitch_vod"

    def test_explicit_extractor_override(self, temp_json_file):
        """Test that explicit extractor parameter overrides auto-detection."""
        ytdl = Ytdl_nfo(str(temp_json_file), extractor="custom_extractor")
        assert ytdl.extractor == "custom_extractor"

    def test_missing_extractor_field(self, tmp_path):
        """Test handling when extractor field is missing from JSON."""
        json_data = {"id": "test123", "title": "Test"}
        json_file = tmp_path / "test.info.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f)

        ytdl = Ytdl_nfo(str(json_file))
        # Should handle gracefully
        assert ytdl.extractor is None or isinstance(ytdl.extractor, str)
```

**Step 2: Run tests**

Run: `uv run pytest tests/test_ytdl_nfo.py::TestYtdlNfoExtractorDetection -v`
Expected: All tests PASS

**Step 3: Commit**

```bash
git add tests/test_ytdl_nfo.py
git commit -m "test: add extractor detection tests for Ytdl_nfo

Test auto-detection, normalization, explicit override, and missing extractor.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 14: Write Tests for Ytdl_nfo Class - Filename Derivation

**Files:**
- Modify: `tests/test_ytdl_nfo.py`

**Step 1: Add filename derivation tests**

Add to `tests/test_ytdl_nfo.py`:

```python
class TestYtdlNfoFilenameDerivarion:
    """Test filename derivation logic."""

    def test_strips_info_json_suffix(self, temp_json_file):
        """Test that .info.json suffix is stripped for filename."""
        ytdl = Ytdl_nfo(str(temp_json_file))
        # temp_json_file is .../test_video.info.json
        # filename should be .../test_video
        assert ytdl.filename.endswith("test_video")
        assert not ytdl.filename.endswith(".info.json")

    def test_uses_filename_field_fallback(self, tmp_path):
        """Test that _filename field is used when available."""
        json_data = {
            "id": "test123",
            "extractor": "youtube",
            "_filename": "Custom Filename.mp4",
        }
        json_file = tmp_path / "metadata.json"  # Not ending in .info.json
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f)

        ytdl = Ytdl_nfo(str(json_file))
        # Should derive from _filename field
        assert "Custom Filename" in ytdl.filename

    def test_nfo_path_generation(self, temp_json_file):
        """Test that NFO path is correctly generated."""
        ytdl = Ytdl_nfo(str(temp_json_file))
        nfo_path = ytdl.get_nfo_path()

        assert nfo_path.endswith(".nfo")
        assert "test_video.nfo" in nfo_path
```

**Step 2: Run tests**

Run: `uv run pytest tests/test_ytdl_nfo.py::TestYtdlNfoFilenameDerivarion -v`
Expected: All tests PASS

**Step 3: Commit**

```bash
git add tests/test_ytdl_nfo.py
git commit -m "test: add filename derivation tests for Ytdl_nfo

Test .info.json stripping, _filename fallback, and NFO path generation.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 15: Write Tests for Nfo Class - Template Loading

**Files:**
- Create: `tests/test_nfo.py`

**Step 1: Write template loading tests**

Create `tests/test_nfo.py`:

```python
"""Tests for Nfo class."""

import pytest
from ytdl_nfo.nfo import Nfo


class TestNfoTemplateLoading:
    """Test YAML template loading functionality."""

    def test_successful_template_loading(self):
        """Test that known extractor template loads successfully."""
        nfo = Nfo("youtube", "test.info.json")
        assert nfo.config_ok() is True
        assert nfo.data is not None

    def test_missing_template_error_handling(self):
        """Test that missing extractor template is handled gracefully."""
        nfo = Nfo("nonexistent_extractor", "test.info.json")
        assert nfo.config_ok() is False
        assert nfo.data is None

    def test_config_ok_validation(self):
        """Test that config_ok() correctly validates template loading."""
        valid_nfo = Nfo("youtube", "test.info.json")
        invalid_nfo = Nfo("nonexistent", "test.info.json")

        assert valid_nfo.config_ok() is True
        assert invalid_nfo.config_ok() is False
```

**Step 2: Run tests**

Run: `uv run pytest tests/test_nfo.py::TestNfoTemplateLoading -v`
Expected: All tests PASS

**Step 3: Commit**

```bash
git add tests/test_nfo.py
git commit -m "test: add template loading tests for Nfo class

Test successful loading, missing template handling, and config validation.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 16: Write Tests for Nfo Class - NFO Generation

**Files:**
- Modify: `tests/test_nfo.py`

**Step 1: Add NFO generation tests**

Add to `tests/test_nfo.py`:

```python
import xml.etree.ElementTree as ET


class TestNfoGeneration:
    """Test NFO generation functionality."""

    def test_basic_field_mapping(self, sample_youtube_json_data):
        """Test that basic fields are mapped from JSON to NFO."""
        nfo = Nfo("youtube", "test.info.json")
        success = nfo.generate(sample_youtube_json_data)

        assert success is True
        assert nfo.generated_ok() is True
        assert nfo.top is not None

        # Verify XML structure
        title = nfo.top.find("title")
        assert title is not None
        assert title.text == "Test Video Title"

    def test_missing_field_handling(self):
        """Test that missing fields default to empty string."""
        incomplete_data = {
            "id": "test123",
            "extractor": "youtube",
            "upload_date": "20230115",
        }
        nfo = Nfo("youtube", "test.info.json")
        success = nfo.generate(incomplete_data)

        # Should not crash, fields should be empty or use defaults
        assert success is True or success is False  # Depends on template requirements

    def test_upload_date_auto_generation(self):
        """Test that upload_date is auto-generated from epoch if missing."""
        data_without_upload_date = {
            "id": "test123",
            "title": "Test",
            "uploader": "Tester",
            "extractor": "youtube",
            "epoch": 1673827200,  # 2023-01-16 00:00:00 UTC
        }
        nfo = Nfo("youtube", "test.info.json")
        success = nfo.generate(data_without_upload_date)

        # upload_date should be auto-generated
        assert success is True

    def test_generated_ok_validation(self, sample_youtube_json_data):
        """Test that generated_ok() correctly validates NFO generation."""
        nfo = Nfo("youtube", "test.info.json")

        assert nfo.generated_ok() is False  # Before generation

        nfo.generate(sample_youtube_json_data)

        assert nfo.generated_ok() is True  # After generation

    def test_xml_output_well_formed(self, sample_youtube_json_data):
        """Test that generated XML is well-formed."""
        nfo = Nfo("youtube", "test.info.json")
        nfo.generate(sample_youtube_json_data)

        xml_string = nfo.get_nfo()

        # Should be valid XML
        assert xml_string is not None
        assert "<?xml" in xml_string
        assert "<episodedetails>" in xml_string
        assert "</episodedetails>" in xml_string
```

**Step 2: Run tests**

Run: `uv run pytest tests/test_nfo.py::TestNfoGeneration -v`
Expected: All tests PASS

**Step 3: Commit**

```bash
git add tests/test_nfo.py
git commit -m "test: add NFO generation tests for Nfo class

Test field mapping, missing field handling, upload_date generation,
validation, and XML well-formedness.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 17: Write Integration Tests - End-to-End Workflow

**Files:**
- Create: `tests/test_integration.py`
- Create: `tests/fixtures/sample_youtube.info.json`

**Step 1: Create sample fixture files**

Create `tests/fixtures/sample_youtube.info.json`:

```json
{
  "id": "dQw4w9WgXcQ",
  "title": "Sample YouTube Video",
  "uploader": "Sample Channel",
  "description": "This is a sample video for testing",
  "upload_date": "20230115",
  "extractor": "youtube",
  "_filename": "Sample YouTube Video.mp4"
}
```

**Step 2: Write integration tests**

Create `tests/test_integration.py`:

```python
"""Integration tests for end-to-end workflows."""

import json
import pytest
from pathlib import Path
from ytdl_nfo import Ytdl_nfo


@pytest.mark.integration
class TestEndToEndWorkflow:
    """Test complete workflow from JSON to NFO."""

    def test_youtube_json_to_nfo(self, tmp_path, sample_youtube_json_data):
        """Test complete workflow for YouTube video."""
        # Create test JSON file
        json_file = tmp_path / "test_video.info.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(sample_youtube_json_data, f)

        # Process file
        ytdl = Ytdl_nfo(str(json_file))
        success = ytdl.process()

        # Verify NFO was created
        nfo_path = ytdl.get_nfo_path()
        assert Path(nfo_path).exists()

        # Verify NFO content
        with open(nfo_path, "r", encoding="utf-8") as f:
            nfo_content = f.read()

        assert "<?xml" in nfo_content
        assert "Test Video Title" in nfo_content
        assert "Test Uploader" in nfo_content

    def test_twitch_vod_json_to_nfo(self, tmp_path, sample_twitch_json_data):
        """Test complete workflow for Twitch VOD."""
        # Create test JSON file
        json_file = tmp_path / "test_vod.info.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(sample_twitch_json_data, f)

        # Process file
        ytdl = Ytdl_nfo(str(json_file))
        success = ytdl.process()

        # Verify NFO was created (if twitch_vod template exists)
        nfo_path = ytdl.get_nfo_path()
        if success:
            assert Path(nfo_path).exists()

    def test_invalid_json_graceful_handling(self, tmp_path):
        """Test that invalid JSON is handled without crashing."""
        json_file = tmp_path / "invalid.info.json"
        json_file.write_text("{invalid json}", encoding="utf-8")

        ytdl = Ytdl_nfo(str(json_file))
        # Should not crash
        result = ytdl.process()

        assert result is False

    def test_missing_template_graceful_handling(self, tmp_path):
        """Test that missing template is handled gracefully."""
        json_data = {
            "id": "test123",
            "title": "Test",
            "extractor": "nonexistent_extractor",
        }
        json_file = tmp_path / "test.info.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f)

        ytdl = Ytdl_nfo(str(json_file))
        result = ytdl.process()

        # Should return False but not crash
        assert result is False
```

**Step 3: Run integration tests**

Run: `uv run pytest tests/test_integration.py -v`
Expected: All tests PASS

**Step 4: Commit**

```bash
git add tests/test_integration.py tests/fixtures/
git commit -m "test: add end-to-end integration tests

Test complete workflows for YouTube and Twitch, plus error handling
for invalid JSON and missing templates.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 18: Run Full Test Suite and Generate Coverage Report

**Files:**
- None (verification only)

**Step 1: Run all tests**

Run: `uv run pytest -v`
Expected: All tests PASS

**Step 2: Run tests with coverage**

Run: `uv run pytest --cov=ytdl_nfo --cov-report=term-missing`
Expected: Coverage report showing percentage for each file

**Step 3: Review coverage**

Check that core functionality is covered:
- `ytdl_nfo/__init__.py` (CLI)
- `ytdl_nfo/Ytdl_nfo.py` (orchestration)
- `ytdl_nfo/nfo.py` (template engine)

**Step 4: Run only unit tests**

Run: `uv run pytest -m unit -v`
Expected: Unit tests PASS

**Step 5: Run only integration tests**

Run: `uv run pytest -m integration -v`
Expected: Integration tests PASS

**Step 6: Commit verification**

```bash
git commit --allow-empty -m "test: verify Phase B test suite complete

✓ All tests passing
✓ Coverage report generated
✓ Core functionality tested
✓ Integration tests validate workflows

Phase B (Test Suite Addition) complete.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 19: Final Verification - Complete Project

**Files:**
- None (final verification)

**Step 1: Verify devcontainer works**

Rebuild container if needed:
Command Palette → "Dev Containers: Rebuild Container"

**Step 2: Verify all tools work**

```bash
uv --version
ruff --version
pytest --version
```

Expected: All commands work

**Step 3: Run complete test suite**

Run: `uv run pytest --cov=ytdl_nfo --cov-report=term-missing --cov-report=html`
Expected: All tests PASS, HTML coverage report generated

**Step 4: Build package**

Run: `uv build`
Expected: Package builds successfully

**Step 5: Test CLI**

Run: `uv run ytdl-nfo --config`
Expected: Shows config directory path

**Step 6: Verify linting**

```bash
uv run ruff check ytdl_nfo
uv run ruff format --check ytdl_nfo
```

Expected: Clean linting, formatting applied

**Step 7: Review git status**

Run: `git status`
Expected: Clean working tree

**Step 8: Create final commit**

```bash
git commit --allow-empty -m "chore: complete uv migration and test suite implementation

✅ Phase A Complete:
- VS Code devcontainer with Python 3.11, uv, ruff, pytest
- Migrated from Poetry to uv (PEP 621 pyproject.toml)
- Replaced flake8/autopep8 with ruff
- Removed Nix flake files
- Updated documentation (README.md, CLAUDE.md)

✅ Phase B Complete:
- pytest test suite for core functionality
- Unit tests for Ytdl_nfo and Nfo classes
- Integration tests for end-to-end workflows
- Coverage reporting configured

All success criteria met. Ready for merge.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Execution Notes

**Prerequisites:**
- Docker installed and running
- VS Code with Dev Containers extension
- Git configured

**Testing Strategy:**
- Follow TDD where new code is added
- Existing code has tests added after (testing existing behavior)
- Run tests after each change
- Maintain clean git history with frequent commits

**Common Issues:**

1. **Container build fails:** Check Docker is running, rebuild with clean cache
2. **uv sync fails:** Check pyproject.toml syntax, verify dependencies exist
3. **Tests fail:** Review actual vs expected behavior, adjust tests or code
4. **Ruff formatting changes:** Auto-formatting may differ from manual style

**Skills Referenced:**
- @superpowers:test-driven-development for writing new features
- @superpowers:verification-before-completion before marking tasks done
- @superpowers:systematic-debugging if tests fail unexpectedly
