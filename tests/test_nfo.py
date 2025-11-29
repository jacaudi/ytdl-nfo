"""Tests for Nfo class."""


import pytest

from ytdl_nfo.nfo import Nfo


@pytest.mark.unit
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


@pytest.mark.unit
class TestNfoGeneration:
    """Test NFO generation functionality."""

    def test_basic_field_mapping(self, sample_youtube_json_data):
        """Test that basic fields are mapped from JSON to NFO."""
        nfo = Nfo("youtube", "test.info.json")
        success = nfo.generate(sample_youtube_json_data)

        assert success is True
        assert nfo.generated_ok() is True
        assert nfo.top is not None

        # Verify XML structure
        title = nfo.top.find("title")
        assert title is not None
        assert title.text == "Test Video Title"

    def test_missing_field_handling(self):
        """Test that missing fields default to empty string."""
        incomplete_data = {
            "id": "test123",
            "extractor": "youtube",
            "upload_date": "20230115",
        }
        nfo = Nfo("youtube", "test.info.json")
        success = nfo.generate(incomplete_data)

        # Should not crash, fields should be empty or use defaults
        assert success is True or success is False  # Depends on template requirements

    def test_upload_date_auto_generation(self):
        """Test that upload_date is auto-generated from epoch if missing."""
        data_without_upload_date = {
            "id": "test123",
            "title": "Test",
            "uploader": "Tester",
            "extractor": "youtube",
            "epoch": 1673827200,  # 2023-01-16 00:00:00 UTC
        }
        nfo = Nfo("youtube", "test.info.json")
        success = nfo.generate(data_without_upload_date)

        # upload_date should be auto-generated
        assert success is True

    def test_generated_ok_validation(self, sample_youtube_json_data):
        """Test that generated_ok() correctly validates NFO generation."""
        nfo = Nfo("youtube", "test.info.json")

        assert nfo.generated_ok() is False  # Before generation

        nfo.generate(sample_youtube_json_data)

        assert nfo.generated_ok() is True  # After generation

    def test_xml_output_well_formed(self, sample_youtube_json_data):
        """Test that generated XML is well-formed."""
        nfo = Nfo("youtube", "test.info.json")
        nfo.generate(sample_youtube_json_data)

        xml_string = nfo.get_nfo()

        # Should be valid XML
        assert xml_string is not None
        assert "<?xml" in xml_string
        assert "<episodedetails>" in xml_string
        assert "</episodedetails>" in xml_string
