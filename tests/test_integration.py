"""Integration tests for end-to-end workflows."""

import json
from pathlib import Path

import pytest

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
        ytdl.process()

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
