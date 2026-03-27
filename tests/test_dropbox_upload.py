"""Test dropbox_upload.py modular functions.

Tests parse_args, should_skip_file, and other pure functions
that can be tested without hardware dependencies.
"""
import sys
import os

# Add repo root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Mock dropbox before importing
from unittest.mock import MagicMock
sys.modules['dropbox'] = MagicMock()
sys.modules['dropbox.files'] = MagicMock()
sys.modules['dropbox.exceptions'] = MagicMock()

import dropbox_upload


def test_parse_args_default_values():
    """Test parse_args with default values."""
    args = dropbox_upload.parse_args([])
    assert args.folder == 'Downloads'
    assert args.rootdir == '~/Downloads'
    assert args.token == dropbox_upload.TOKEN
    assert args.yes is False
    assert args.no is False
    assert args.default is False
    assert args.count is None


def test_parse_args_with_options():
    """Test parse_args with various command-line options."""
    args = dropbox_upload.parse_args(['--count', '10', '--yes', 'Photos', '/tmp'])
    assert args.count == 10
    assert args.yes is True
    assert args.folder == 'Photos'


def test_should_skip_file_dot_files():
    """Test that dot files are skipped."""
    assert dropbox_upload.should_skip_file('.gitignore') is True
    assert dropbox_upload.should_skip_file('.hidden') is True
    assert dropbox_upload.should_skip_file('.bashrc') is True


def test_should_skip_file_temp_files():
    """Test that temporary files are skipped."""
    assert dropbox_upload.should_skip_file('file.tmp') is True
    assert dropbox_upload.should_skip_file('file.temp') is True
    assert dropbox_upload.should_skip_file('~backup') is True
    assert dropbox_upload.should_skip_file('@temp') is True


def test_should_skip_file_generated_files():
    """Test that generated files are skipped."""
    assert dropbox_upload.should_skip_file('test.pyc') is True
    assert dropbox_upload.should_skip_file('test.pyo') is True
    assert dropbox_upload.should_skip_file('__pycache__') is True


def test_should_skip_file_empty_and_none():
    """Test that empty strings and None are skipped."""
    assert dropbox_upload.should_skip_file(None) is True
    assert dropbox_upload.should_skip_file('') is True


def test_should_skip_file_normal_files():
    """Test that normal files are not skipped."""
    assert dropbox_upload.should_skip_file('photo.jpg') is False
    assert dropbox_upload.should_skip_file('document.pdf') is False
    assert dropbox_upload.should_skip_file('video.mp4') is False


def test_should_skip_file_case_sensitive():
    """Test that file filtering is case-sensitive."""
    # .PYC is NOT filtered because check is case-sensitive
    assert dropbox_upload.should_skip_file('test.PYC') is False
    assert dropbox_upload.should_skip_file('image.JPG') is False


def test_should_skip_file_non_string():
    """Test handling of non-string input."""
    assert dropbox_upload.should_skip_file(123) is False  # Convertible to string
    assert dropbox_upload.should_skip_file(['list']) is False  # List converts to 'list' string
