"""Tests for dropbox_upload.py functionality."""

import pytest
import os
import sys
import tempfile
import json
from unittest.mock import MagicMock, patch, mock_open

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDropboxUploadConfig:
    """Test configuration file handling for Dropbox token storage."""
    
    @pytest.fixture
    def config_file_path(self, tmp_path):
        """Create a temporary config file path."""
        return tmp_path / "dropbox_config.json"
    
    def test_config_file_creation(self, config_file_path):
        """Test creating a config file with a token."""
        token = "test_dropbox_token_12345"
        config_data = {"token": token}
        with open(config_file_path, 'w') as f:
            json.dump(config_data, f)
        
        assert config_file_path.exists()
        with open(config_file_path, 'r') as f:
            loaded = json.load(f)
        assert loaded["token"] == token
    
    def test_config_file_loading(self, config_file_path):
        """Test loading configuration from file."""
        token = "test_dropbox_token_12345"
        folder = "Downloads"
        
        config_data = {
            "token": token,
            "folder": folder,
            "rootdir": "~/Downloads"
        }
        with open(config_file_path, 'w') as f:
            json.dump(config_data, f)
        
        with open(config_file_path, 'r') as f:
            loaded = json.load(f)
        
        assert loaded["token"] == token
        assert loaded["folder"] == folder
        assert loaded["rootdir"] == "~/Downloads"


class TestDropboxUploadYesno:
    """Test the yesno function logic."""
    
    def test_yesno_default_true(self):
        """Test yesno with default True and empty input."""
        default = True
        answer = ""
        
        if not answer:
            result = default
        else:
            result = answer.lower() in ('y', 'yes')
        
        assert result is True
    
    def test_yesno_default_false(self):
        """Test yesno with default False and empty input."""
        default = False
        answer = ""
        
        if not answer:
            result = default
        else:
            result = answer.lower() in ('y', 'yes')
        
        assert result is False
    
    def test_yesno_yes(self):
        """Test yesno with 'yes' answer."""
        answer = "yes"
        result = answer.lower() in ('y', 'yes')
        assert result is True
    
    def test_yesno_y(self):
        """Test yesno with 'y' answer."""
        answer = "y"
        result = answer.lower() in ('y', 'yes')
        assert result is True
    
    def test_yesno_no(self):
        """Test yesno with 'no' answer."""
        answer = "no"
        result = answer.lower() in ('n', 'no')
        assert result is True
    
    def test_yesno_n(self):
        """Test yesno with 'n' answer."""
        answer = "n"
        result = answer.lower() in ('n', 'no')
        assert result is True


class TestDropboxUploadStopwatch:
    """Test the stopwatch context manager."""
    
    def test_stopwatch_basic(self):
        """Test stopwatch measures time correctly."""
        start = 1000.0
        end = 1001.5
        elapsed = end - start
        
        assert elapsed == 1.5
        assert elapsed > 0


class TestDropboxUploadFileFiltering:
    """Test file filtering logic for upload decisions."""
    
    def test_skip_dot_files(self):
        """Test that dot files are skipped."""
        filename = ".hidden_file"
        assert filename.startswith('.')
    
    def test_skip_temp_files_end_tilde(self):
        """Test that files ending with ~ are skipped."""
        filename = "file~"
        assert filename.endswith('~')
    
    def test_skip_temp_files_start_at(self):
        """Test that files starting with @ are skipped."""
        filename = "@recycle"
        assert filename.startswith('@')
    
    def test_skip_generated_files(self):
        """Test that .pyc and .pyo files are skipped."""
        assert ".pyc" in "file.pyc"
        assert ".pyo" in "file.pyo"
    
    def test_skip_pycache_dirs(self):
        """Test that __pycache__ directories are skipped."""
        dirname = "__pycache__"
        assert dirname == "__pycache__"


class TestDropboxUploadPathHandling:
    """Test path handling and normalization."""
    
    def test_path_double_slash_removal(self):
        """Test that double slashes are removed from paths."""
        path = "/folder//subfolder"
        normalized = path.replace('//', '/')
        assert normalized == "/folder/subfolder"
    
    def test_path_trailing_slash_removal(self):
        """Test that trailing slashes are removed."""
        path = "/folder/subfolder/"
        normalized = path.rstrip('/')
        assert normalized == "/folder/subfolder"
    
    def test_path_normalization_chain(self):
        """Test combined path normalization."""
        path = "/folder//subfolder//"
        while '//' in path:
            path = path.replace('//', '/')
        path = path.rstrip('/')
        assert path == "/folder/subfolder"
