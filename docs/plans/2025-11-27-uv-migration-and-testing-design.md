# ytdl-nfo Refactoring: uv Migration and Test Suite Addition

**Date:** 2025-01-27
**Status:** Design Approved
**Approach:** Sequential refactoring (migration first, then tests)

## Overview

This design document outlines the refactoring of ytdl-nfo to:
1. Set up VS Code Dev Container for containerized development
2. Migrate from Poetry to uv for dependency management and tooling
3. Replace flake8/autopep8 with ruff for linting and formatting
4. Remove Nix/flakes development environment
5. Add comprehensive pytest-based test suite for core functionality

## Goals

- **Consistency**: Containerized development environment ensures identical setup across all machines
- **Performance**: Faster dependency resolution and package operations via uv
- **Simplicity**: Reduced tooling complexity and configuration overhead
- **Modern Standards**: PEP 621 compliance and alignment with Python ecosystem direction
- **Quality**: Test coverage for critical paths to prevent regressions
- **Clean Migration**: Complete transition with no Poetry or Nix remnants

## Design Decisions

### Migration Strategy
**Sequential approach**: Complete tooling migration first, then add test suite.

**Rationale**: Clean separation of concerns allows independent validation of each phase. Migration changes are isolated from test development, making it easier to verify the tooling switch didn't break existing functionality.

### Test Framework
**pytest** with pytest-cov for coverage reporting.

**Rationale**: Industry standard, rich plugin ecosystem, powerful fixtures, excellent for this codebase size. More expressive and less verbose than unittest.

### Test Coverage Scope
**Core functionality only**: Focus on critical paths rather than comprehensive coverage.

**Coverage targets**:
- JSON parsing and validation
- Extractor detection and normalization
- NFO generation and template processing
- File I/O operations
- End-to-end workflows with sample data

**Out of scope**: CLI argument edge cases, exhaustive error condition testing.

### Linting Modernization
**ruff** replaces flake8 and autopep8.

**Rationale**: All-in-one tool (linter + formatter), significantly faster, increasingly becoming the Python ecosystem standard, simpler configuration.

### Development Environment
**VS Code Dev Container** with full development environment.

**Rationale**: Ensures consistent development environment across all machines, eliminates "works on my machine" issues, pre-installs all tools (Python, uv, ruff, pytest), provides seamless VS Code integration.

## Architecture

### Two-Phase Structure

#### Phase A: Tooling Migration + Containerization
Set up dev container and complete migration from Poetry/Nix to uv/ruff ecosystem.

#### Phase B: Test Suite Addition
Build pytest-based test suite on the new foundation (inside container).

## Phase A: Tooling Migration + Containerization

### 1. Create VS Code Dev Container

**Create `.devcontainer/` directory structure:**
- `.devcontainer/devcontainer.json` - VS Code configuration
- `.devcontainer/Dockerfile` - Container image definition

**Dockerfile specifications:**
- Base image: `python:3.8-slim` (or later)
- Install uv: Latest version via official installer
- Install ruff: Via pip or uv
- Install pytest and pytest-cov: Via pip or uv
- Set up working directory
- Configure Python environment

**devcontainer.json specifications:**
- Name: "ytdl-nfo Python Development"
- Build from Dockerfile
- VS Code extensions: Python, Pylance, Ruff
- Settings: Configure Python interpreter, enable ruff linter/formatter
- Post-create command: `uv sync` to install dependencies
- Features: Git (if needed)

### 2. Remove Nix Development Environment

**Files to delete:**
- `flake.nix`
- `flake.lock`

**Documentation updates:**
- Remove Nix setup instructions from README.md
- Replace Nix section with devcontainer instructions in README.md
- Remove Nix alternative from CLAUDE.md development environment section
- Add devcontainer workflow to CLAUDE.md

### 3. Update pyproject.toml

**Convert to PEP 621 standard format:**

Current Poetry-specific sections:
```toml
[tool.poetry.group.dev]
optional = true

[tool.poetry.group.dev.dependencies]
flake8 = "^5.0.4"
autopep8 = "^1.6.0"
```

New uv-compatible format:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
]
```

**Add ruff configuration:**
```toml
[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Build system:**
Keep existing or adjust based on uv recommendations:
```toml
[build-system]
requires = ["hatchling"]  # or poetry-core if maintaining compatibility
build-backend = "hatchling.build"  # or poetry.core.masonry.api
```

### 3. Dependency Management

**Runtime dependencies (unchanged):**
- PyYAML>=6.0.1
- setuptools>=70.2.0

**Development dependencies (new):**
- pytest>=8.0.0
- pytest-cov>=4.1.0
- ruff>=0.1.0

**Migration commands:**
```bash
# Initialize uv project
uv init

# Add dev dependencies
uv add --dev pytest pytest-cov ruff

# Generate lock file
uv lock

# Verify installation
uv sync
```

### 4. Update Documentation

**README.md changes:**
- Add devcontainer setup instructions
- Replace Poetry installation instructions with uv
- Remove Nix development environment section
- Update "Package from Source" to use uv inside container
- Update development commands to run in container context
- Add "Development with VS Code" section explaining container workflow

**CLAUDE.md changes:**
- Add "Development Environment" section for devcontainer
  - Opening project in container
  - Running commands inside container
  - Container rebuild when needed
- Replace Poetry commands with uv equivalents:
  - `poetry install` → `uv sync` (inside container)
  - `poetry shell` → Not needed (already in container)
  - `poetry run ytdl-nfo` → `uv run ytdl-nfo` (inside container)
  - `poetry build` → `uv build` (inside container)
- Update linting section:
  - `poetry run flake8` → `uv run ruff check` (inside container)
  - `poetry run autopep8` → `uv run ruff format` (inside container)
- Remove Nix alternative setup
- Add note that all commands assume running inside devcontainer

### 5. Ruff Configuration

**Linting rules:**
- E: pycodestyle errors
- F: pyflakes
- W: pycodestyle warnings
- I: isort (import sorting)
- N: pep8-naming

**Formatting:**
- Line length: 100 (common Python standard)
- Double quotes (match existing code style)
- Space indentation (existing style)

**Create .ruffignore if needed** for build artifacts, generated files, etc.

### 6. Verification

**Post-migration validation (all commands run inside devcontainer):**
```bash
# Open project in devcontainer (VS Code will prompt)
# Or use: Command Palette → "Dev Containers: Reopen in Container"

# Verify container built successfully and uv is available
uv --version

# Install and verify dependencies
uv sync
uv tree

# Build package
uv build

# Verify CLI works
uv run ytdl-nfo --config

# Run linter
uv run ruff check ytdl_nfo

# Run formatter (check mode)
uv run ruff format --check ytdl_nfo
```

## Phase B: Test Suite Addition

### Directory Structure

```
tests/
├── __init__.py
├── conftest.py                    # Pytest fixtures and shared configuration
├── fixtures/
│   ├── sample_youtube.info.json   # Real youtube-dl output samples
│   ├── sample_twitch.info.json
│   ├── sample_vimeo.info.json
│   ├── expected_youtube.nfo       # Expected NFO output
│   ├── expected_twitch.nfo
│   └── expected_vimeo.nfo
├── test_ytdl_nfo.py               # Ytdl_nfo class unit tests
├── test_nfo.py                    # Nfo class unit tests
└── test_integration.py             # End-to-end integration tests
```

### Test Coverage by Component

#### test_ytdl_nfo.py

**Ytdl_nfo class tests:**

1. **JSON parsing**
   - Valid JSON file loading
   - Invalid JSON error handling
   - Missing file error handling

2. **Extractor detection**
   - Auto-detection from JSON `extractor` field
   - Extractor name normalization (`:?*/\` → `_`, lowercase)
   - Explicit extractor override via constructor parameter
   - Handling missing extractor field

3. **Filename derivation**
   - Stripping `.info.json` suffix
   - Using JSON `_filename` field as fallback
   - Default to input path when both methods fail

4. **NFO path generation**
   - Correct `.nfo` extension appended to base filename

5. **Process workflow**
   - Successful NFO generation and writing
   - Graceful handling when config missing
   - Graceful handling when input invalid

#### test_nfo.py

**Nfo class tests:**

1. **Template loading**
   - Successful YAML config loading for known extractors
   - Error handling for missing extractor templates
   - `config_ok()` validation

2. **NFO generation**
   - Basic field mapping (`{title}`, `{description}`, etc.)
   - Missing field handling (defaultdict behavior → empty string)
   - `generated_ok()` validation after generation

3. **Date conversion**
   - `upload_date` format conversion (input_f → output_f)
   - Auto-generation of `upload_date` from `epoch` when missing

4. **List processing**
   - Fields with `!` suffix create multiple XML elements
   - `ast.literal_eval()` parsing of list values

5. **Nested elements**
   - `>` delimiter creates parent-child structure
   - Validation that `>` only works with lists

6. **Attributes**
   - `attr` key adds XML attributes to elements
   - Attribute value formatting with JSON fields

7. **XML output**
   - Well-formed XML structure
   - Pretty-printing via minidom

#### test_integration.py

**End-to-end workflow tests:**

1. **Full pipeline for each major extractor:**
   - Load real `.info.json` fixture
   - Generate NFO via Ytdl_nfo class
   - Verify output matches expected NFO fixture
   - Test youtube, twitch, vimeo templates minimally

2. **Directory processing simulation:**
   - Multiple JSON files processed
   - Correct NFO files created
   - `.live_chat.json` files skipped

3. **Error scenarios:**
   - Invalid JSON handled gracefully
   - Missing template handled gracefully
   - Missing required JSON fields handled gracefully

### Pytest Configuration

**Add to pyproject.toml:**

```toml
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

### Fixtures Strategy

**conftest.py shared fixtures:**

```python
@pytest.fixture
def sample_youtube_json():
    """Load sample YouTube .info.json data"""
    # Return parsed JSON dict

@pytest.fixture
def sample_youtube_nfo():
    """Load expected YouTube .nfo output"""
    # Return XML string

@pytest.fixture
def temp_json_file(tmp_path):
    """Create temporary JSON file for testing"""
    # Return Path object
```

### Test Execution

**Running tests:**
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=ytdl_nfo --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_nfo.py

# Run specific test
uv run pytest tests/test_nfo.py::test_template_loading

# Run only unit tests
uv run pytest -m unit

# Run only integration tests
uv run pytest -m integration
```

## Migration Checklist

### Phase A: Tooling Migration + Containerization

- [ ] Create `.devcontainer/` directory
- [ ] Create `.devcontainer/Dockerfile` with Python 3.8+, uv, ruff, pytest
- [ ] Create `.devcontainer/devcontainer.json` with VS Code configuration
- [ ] Test devcontainer builds successfully
- [ ] Delete `flake.nix` and `flake.lock`
- [ ] Update `pyproject.toml` to PEP 621 format
- [ ] Add `[project.optional-dependencies]` for dev dependencies
- [ ] Add `[tool.ruff]` configuration
- [ ] Add `[tool.pytest.ini_options]` configuration
- [ ] Open project in devcontainer
- [ ] Run `uv sync` (inside container) to install dependencies and create lock file
- [ ] Delete `poetry.lock`
- [ ] Update README.md (add devcontainer, remove Nix, update Poetry → uv)
- [ ] Update CLAUDE.md (add devcontainer workflow, remove Nix, update commands)
- [ ] Verify build: `uv build` (inside container)
- [ ] Verify CLI: `uv run ytdl-nfo --config` (inside container)
- [ ] Run ruff linter: `uv run ruff check ytdl_nfo` (inside container)
- [ ] Run ruff formatter: `uv run ruff format ytdl_nfo` (inside container)
- [ ] Commit migration changes

### Phase B: Test Suite Addition

- [ ] Create `tests/` directory structure
- [ ] Create `tests/__init__.py`
- [ ] Create `tests/conftest.py` with shared fixtures
- [ ] Create `tests/fixtures/` directory
- [ ] Add sample `.info.json` files for youtube, twitch, vimeo
- [ ] Add expected `.nfo` files for each sample
- [ ] Write `test_ytdl_nfo.py` (JSON parsing, extractor detection, filename handling)
- [ ] Write `test_nfo.py` (template loading, NFO generation, XML output)
- [ ] Write `test_integration.py` (end-to-end workflows)
- [ ] Run tests: `uv run pytest`
- [ ] Verify coverage meets core functionality goal
- [ ] Fix any failing tests
- [ ] Commit test suite

## Success Criteria

**Phase A Complete:**
- ✓ Devcontainer builds successfully
- ✓ VS Code opens project in container
- ✓ uv is available and working inside container
- ✓ No Poetry files remain (`poetry.lock` deleted)
- ✓ No Nix files remain (`flake.nix`, `flake.lock` deleted)
- ✓ `uv sync` successfully installs all dependencies (inside container)
- ✓ `uv build` successfully builds package (inside container)
- ✓ `uv run ytdl-nfo` CLI works correctly (inside container)
- ✓ `uv run ruff check` passes or shows actionable issues (inside container)
- ✓ Documentation reflects new tooling and container workflow

**Phase B Complete:**
- ✓ Test suite runs via `uv run pytest` (inside container)
- ✓ Core functionality tests pass
- ✓ Coverage report shows critical paths tested
- ✓ Integration tests validate end-to-end workflows
- ✓ Fixtures provide realistic test data

## Future Enhancements (Out of Scope)

- CI/CD pipeline setup (GitHub Actions with uv)
- Pre-commit hooks with ruff
- Comprehensive error case testing
- CLI argument validation tests
- Performance benchmarking tests
- Additional extractor template tests
