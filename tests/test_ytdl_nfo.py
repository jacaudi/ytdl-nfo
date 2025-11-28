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
