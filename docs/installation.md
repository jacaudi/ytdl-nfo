# Installation Guide

Complete installation instructions for ytdl-nfo.

## Table of Contents

- [From GitHub Releases](#from-github-releases)
- [From PyPI (Coming Soon)](#from-pypi-coming-soon)
- [For Python Projects](#for-python-projects)
- [Usage Examples](#usage-examples)

## From GitHub Releases

Download the latest `.whl` file from [Releases](https://github.com/jacaudi/ytdl-nfo/releases), then install:

### Using pipx (Recommended for CLI Tools)

```bash
pipx install ytdl_nfo-VERSION-py3-none-any.whl
```

### Using uv

```bash
uv tool install ytdl_nfo-VERSION-py3-none-any.whl
```

### Using pip

```bash
pip install ytdl_nfo-VERSION-py3-none-any.whl
```

**Note:** Replace `VERSION` with the actual version number (e.g., `0.1.0`).

## From PyPI (Coming Soon)

Once published to PyPI, you'll be able to install directly:

```bash
# Using pipx (recommended for CLI tools)
pipx install ytdl-nfo

# Using uv
uv tool install ytdl-nfo

# Using pip
pip install ytdl-nfo
```

## For Python Projects

### From GitHub Releases

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

**Note:** Replace `VERSION` with the actual version number (e.g., `0.1.0`).

### From PyPI (Coming Soon)

**With pip (requirements.txt):**
```
ytdl-nfo
```

**With uv (pyproject.toml):**
```toml
[project]
dependencies = [
    "ytdl-nfo"
]
```

**With Poetry:**
```bash
poetry add ytdl-nfo
```

## Usage Examples

### Basic Usage

```bash
# Display the configuration location
ytdl-nfo --config

# Convert a single video's metadata
ytdl-nfo video.info.json

# Process an entire directory recursively
ytdl-nfo /path/to/videos/
```

### Advanced Options

```bash
# Override extractor auto-detection
ytdl-nfo --extractor youtube video.info.json

# Use custom regex to match files
ytdl-nfo --regex "\.json$" /path/to/videos/

# Overwrite existing NFO files
ytdl-nfo --overwrite /path/to/videos/
```

### Command-Line Options

```
ytdl-nfo [-h] [--config] [-e EXTRACTOR] [--regex REGEX] [-w] JSON_FILE

positional arguments:
  JSON_FILE             JSON file to convert or directory to process recursively

options:
  -h, --help            show this help message and exit
  --config              Show the path to the config directory
  -e EXTRACTOR, --extractor EXTRACTOR
                        Specify specific extractor
  -r, --regex REGEX     A regular expression used to search for JSON source files
  -w, --overwrite       Overwrite existing NFO files
```

## How It Works

yt-dlp uses site-specific extractors to collect technical data about a media file. This metadata, along with the extractor ID, are written to a `.info.json` file when the `--write-info-json` flag is used.

ytdl-nfo uses YAML templates in `ytdl_nfo/configs` to map JSON metadata fields to standardized NFO XML format. Each extractor (youtube, twitch, vimeo, etc.) has its own template file.

If extractor auto-detection fails or you want to override the default, use the `--extractor` option to specify a particular template.

## Verification

After installation, verify ytdl-nfo is installed correctly:

```bash
ytdl-nfo --help
```

You should see the help message with usage instructions.
