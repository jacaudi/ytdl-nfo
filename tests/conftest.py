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
