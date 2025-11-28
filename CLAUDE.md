# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ytdl-nfo converts youtube-dl/yt-dlp JSON metadata files (`.info.json`) to Kodi-compatible NFO files for media centers (Plex, Emby, Jellyfin). It uses a YAML template system to map JSON fields from different video platforms to standardized NFO XML format.

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

## Core Architecture

The codebase follows a three-layer architecture:

### 1. CLI Layer (`ytdl_nfo/__init__.py`)
- Entry point via `main()` function
- Handles argument parsing and file/directory processing
- Recursively walks directories to find `.info.json` files
- Skips `.live_chat.json` files automatically
- Supports custom regex for file matching (`--regex`)

### 2. Orchestration Layer (`ytdl_nfo/Ytdl_nfo.py`)
- **Ytdl_nfo class**: Main controller that:
  - Reads and parses JSON files
  - Auto-detects extractor from JSON `extractor` field
  - Normalizes extractor names (replaces `:?*/\` with `_`, lowercases)
  - Determines output filename by stripping `.info.json` or using `_filename` field
  - Orchestrates NFO generation and file writing

### 3. Template Engine Layer (`ytdl_nfo/nfo.py`)
- **Nfo class**: YAML-based template processor that:
  - Loads extractor-specific YAML configs from `ytdl_nfo/configs/`
  - Recursively transforms YAML template + JSON data → NFO XML
  - Handles missing `upload_date` by deriving from `epoch` timestamp
  - Uses `defaultdict` to allow missing JSON keys (renders as empty string)
  - Writes pretty-printed XML via `minidom`

## YAML Template System

Templates in `ytdl_nfo/configs/` define the NFO structure. Understanding this system is critical for adding new platform support.

### Template Syntax

**Basic field mapping:**
```yaml
episodedetails:
  - title: '{title}'                    # Maps JSON field to XML element
  - plot: '{description}'
```

**Field with attributes:**
```yaml
- uniqueid:
    attr:
      type: 'youtube'
      default: "true"
    value: '{id}'
```

**Date conversion:**
```yaml
- premiered:
    convert: 'date'
    input_f: '%Y%m%d'      # Input format from JSON
    output_f: '%Y-%m-%d'   # Output format for NFO
    value: '{upload_date}'
```

**Lists (note the `!` suffix):**
```yaml
- actor!:                   # ! indicates this creates multiple elements
    value: '{contributors}'  # Must be a Python list in JSON
```

**Nested elements (using `>` delimiter):**
```yaml
- credits>name!:            # Creates <credits><name>value</name></credits>
    value: '{contributors}'
```

### Template Processing Rules

1. All `{field}` placeholders use `.format_map()` with JSON data
2. Missing fields default to empty string (no KeyError)
3. Lists (marked with `!`) are evaluated via `ast.literal_eval()`
4. Nested paths with `>` only work with lists (validation enforced)
5. `upload_date` is auto-generated from `epoch` if missing

## Adding Support for New Platforms

To add a new extractor:

1. Determine the extractor ID (check `.info.json` `extractor` field)
2. Create `ytdl_nfo/configs/<extractor_name>.yaml`
3. Map JSON fields to appropriate NFO elements (see existing templates)
4. Test with: `ytdl-nfo --extractor <extractor_name> <test_file>.info.json`

Common extractor templates already exist for:
- youtube, youtube_tab
- twitch_vod, twitch_clips
- vimeo
- bilibili
- nebula_video, nebula_channel
- zype

## Running the Application

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

## Code Organization

```
ytdl_nfo/
├── __init__.py         # CLI entry point, argument parsing, main()
├── __main__.py         # Allows `python -m ytdl_nfo` execution
├── Ytdl_nfo.py         # Main controller class
├── nfo.py              # Template engine and NFO generator
└── configs/            # YAML templates per extractor
    ├── youtube.yaml
    ├── twitch_vod.yaml
    └── ...
```

## Key Implementation Details

- **Extractor normalization**: Characters `:?*/\` are replaced with `_` and lowercased
- **Filename determination**: Strips `.info.json` suffix or uses JSON `_filename` field
- **Error handling**: Gracefully handles missing configs, invalid JSON, and missing fields
- **XML generation**: Uses `xml.etree.ElementTree` for construction, `minidom` for formatting
- **Package resources**: Templates loaded via `pkg_resources.resource_stream()`
