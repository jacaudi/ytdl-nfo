"""Tests for Ytdl_nfo class."""

import json
import pytest
from ytdl_nfo import Ytdl_nfo


@pytest.mark.unit
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


@pytest.mark.unit
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


@pytest.mark.unit
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
