# ytdl-nfo : yt-dlp NFO generator

Converts [yt-dlp](https://github.com/yt-dlp/yt-dlp) / [youtube-dl](https://github.com/ytdl-org/youtube-dl) metadata to Kodi-compatible `.nfo` files for media centers like Plex, Emby, and Jellyfin.

## Installation

Download the latest `.whl` from [Releases](https://github.com/jacaudi/ytdl-nfo/releases):

```bash
pipx install ytdl_nfo-VERSION-py3-none-any.whl
```

**See [docs/installation.md](docs/installation.md) for complete installation options** (uv, pip, Python projects, PyPI).

## Quick Start

```bash
# Convert a single video's metadata
ytdl-nfo video.info.json

# Process an entire directory
ytdl-nfo /path/to/videos/

# Override extractor auto-detection
ytdl-nfo --extractor youtube video.info.json
```

Run `ytdl-nfo --help` for all options.

## How It Works

ytdl-nfo uses YAML templates to map `.info.json` fields from yt-dlp extractors to Kodi NFO format. Extractor auto-detection works automatically, or specify one with `--extractor`.

## Contributing

Contributions welcome! Please feel free to open issues or pull requests on GitHub.
