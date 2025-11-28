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
