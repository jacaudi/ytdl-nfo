# ytdl-nfo : yt-dlp NFO generator

[yt-dlp](https://github.com/yt-dlp/yt-dlp) is an incredibly useful tool for downloading and archiving footage from across the web. **ytdl-nfo** automates metadata processing so that media files can be easily imported into media centers such as [Plex](https://www.plex.tv/), [Emby](https://emby.media/), [Jellyfin](https://jellyfin.org/), etc. It does this by parsing each `.info.json` file created by yt-dlp (using the `--write-info-json` flag) and generating a Kodi-compatible `.nfo` file.

While this package is built for yt-dlp, it maintains compatibility with [youtube-dl](https://github.com/ytdl-org/youtube-dl).

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

**Note:** Replace `VERSION` with the actual version number (e.g., `0.1.0`).

## Usage

yt-dlp uses site-specific extractors to collect technical data about a media file. This metadata, along with the extractor ID, are written to a `.info.json` file when the `--write-info-json` flag is used. ytdl-nfo uses YAML templates in `ytdl_nfo/configs` to map JSON metadata to NFO tags.

If extractor auto-detection fails or you want to override the default, use the `--extractor` option to specify a particular template.

```text
python3 -m ytdl_nfo [-h] [--config] [-e EXTRACTOR] [--regex REGEX] [-w] JSON_FILE

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

### Examples

```bash
# Display the configuration location
ytdl-nfo --config

# Create a single NFO file using metadata from `great_video.info.json`
ytdl-nfo great_video.info.json

# Create an NFO file for each `.info.json` file located in the `video_folder` directory
# (provided a matching extractor template exists in the `ytdl_nfo/configs` directory)
ytdl-nfo video_folder

# Create a single NFO file using metadata from `great_video.info.json` and the `custom_extractor_name` template
ytdl-nfo --extractor custom_extractor_name great_video.info.json
```

## Contributing

Contributions are welcome! This project uses VS Code Dev Containers for consistent development environments. See `CLAUDE.md` for development setup instructions.
