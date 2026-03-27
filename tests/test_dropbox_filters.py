"""Test dropbox_upload.py file filtering logic."""
import pytest


def test_should_skip_file_dot_files(source_module):
    """Test that dot files are skipped."""
    assert source_module.should_skip_file('.hidden_file') is True
    assert source_module.should_skip_file('.gitignore') is True
    assert source_module.should_skip_file('.DS_Store') is True


def test_should_skip_file_temp_files(source_module):
    """Test that temporary files are skipped."""
    # Skip files ending with .tmp or .temp
    assert source_module.should_skip_file('file.tmp') is True
    assert source_module.should_skip_file('file.temp') is True
    # Skip Mac OS temporary files (starting with ~)
    assert source_module.should_skip_file('~backup') is True
    assert source_module.should_skip_file('@recycled') is True


def test_should_skip_file_generated_files(source_module):
    """Test that generated files are skipped."""
    assert source_module.should_skip_file('file.pyo') is True
    assert source_module.should_skip_file('module.pyc') is True
    assert source_module.should_skip_file('script.pyo') is True


def test_should_skip_file_pycache_dir(source_module):
    """Test that __pycache__ directories are skipped."""
    assert source_module.should_skip_file('__pycache__') is True
    assert source_module.should_skip_file('__pycache__/module.pyc') is True


def test_should_skip_file_empty_string(source_module):
    """Test that empty filenames are skipped."""
    assert source_module.should_skip_file('') is True


def test_should_skip_file_none(source_module):
    """Test that None filenames are skipped."""
    assert source_module.should_skip_file(None) is True


def test_should_not_skip_normal_files(source_module):
    """Test that normal files are not skipped."""
    assert source_module.should_skip_file('photo.jpg') is False
    assert source_module.should_skip_file('image.png') is False
    assert source_module.should_skip_file('document.pdf') is False
    assert source_module.should_skip_file('video.mp4') is False


def test_should_skip_file_case_sensitive(source_module):
    """Test that filtering is case sensitive."""
    # These should NOT be skipped (different case)
    assert source_module.should_skip_file('file.JPG') is False
    assert source_module.should_skip_file('FILE.pyc') is True  # lowercase check


def test_parse_args_basic(source_module):
    """Test basic argument parsing."""
    args = source_module.parse_args(['folder', 'rootdir'])
    assert args.folder == 'folder'
    assert args.rootdir == 'rootdir'


def test_parse_args_with_count(source_module):
    """Test --count argument parsing."""
    args = source_module.parse_args(['folder', 'rootdir', '--count', '5'])
    assert args.folder == 'folder'
    assert args.rootdir == 'rootdir'
    assert args.count == 5


def test_parse_args_yes_no_flags(source_module):
    """Test --yes and --no flags."""
    args = source_module.parse_args(['folder', 'rootdir', '--yes'])
    assert args.yes is True
    assert args.no is False

    args = source_module.parse_args(['folder', 'rootdir', '--no'])
    assert args.no is True
    assert args.yes is False


def test_parse_args_default_folder(source_module):
    """Test default folder argument."""
    args = source_module.parse_args(['rootdir'])
    assert args.folder == 'rootdir'


def test_parse_args_default_rootdir(source_module):
    """Test default rootdir argument."""
    args = source_module.parse_args(['folder'])
    assert args.folder == 'folder'
    assert args.rootdir == '~/Downloads'
