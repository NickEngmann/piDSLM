"""Tests for dropbox_upload.py modular functions."""
import pytest
import sys
import os

# Add repo root to path for direct imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dropbox_upload import should_skip_file, should_skip_directory


def test_should_skip_file_dot_file():
    """Test that dot files are skipped."""
    assert should_skip_file('.hidden') is True
    assert should_skip_file('.gitignore') is True
    assert should_skip_file('.bashrc') is True


def test_should_skip_file_temp_file():
    """Test that temporary files are skipped."""
    assert should_skip_file('@lock') is True
    assert should_skip_file('file.tmp~') is True
    assert should_skip_file('~backup') is True


def test_should_skip_file_generated_file():
    """Test that generated files are skipped."""
    assert should_skip_file('module.pyc') is True
    assert should_skip_file('script.pyo') is True


def test_should_skip_file_regular_file():
    """Test that regular files are NOT skipped."""
    assert should_skip_file('image.jpg') is False
    assert should_skip_file('video.mp4') is False
    assert should_skip_file('document.pdf') is False
    assert should_skip_file('normal_file.txt') is False


def test_should_skip_directory_dot_directory():
    """Test that dot directories are skipped."""
    assert should_skip_directory('.git') is True
    assert should_skip_directory('.cache') is True
    assert should_skip_directory('.svn') is True


def test_should_skip_directory_temp_directory():
    """Test that temporary directories are skipped."""
    assert should_skip_directory('@tmp') is True
    assert should_skip_directory('folder~') is True


def test_should_skip_directory_pycache():
    """Test that __pycache__ directories are skipped."""
    assert should_skip_directory('__pycache__') is True


def test_should_skip_directory_regular_directory():
    """Test that regular directories are NOT skipped."""
    assert should_skip_directory('photos') is False
    assert should_skip_directory('videos') is False
    assert should_skip_directory('documents') is False


def test_should_skip_directory_complex_name():
    """Test edge cases with complex directory names."""
    assert should_skip_directory('my_folder.backup~') is True
    assert should_skip_directory('@temp_folder') is True
