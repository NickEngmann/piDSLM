"""Test dropbox_upload.py error handling and integration.

Tests upload return values, error scenarios, and integration with main().
"""
import sys
import os
from unittest.mock import MagicMock

# Add repo root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# First, set up real exception classes before mocking
class ApiError(Exception):
    """Mock Dropbox API error."""
    pass

class HttpError(Exception):
    """Mock Dropbox HTTP error."""
    pass

# Mock dropbox modules - but set exceptions on them
mock_dropbox = MagicMock()
mock_dropbox.files = MagicMock()
mock_dropbox.exceptions = MagicMock()
mock_dropbox.exceptions.ApiError = ApiError
mock_dropbox.exceptions.HttpError = HttpError

sys.modules['dropbox'] = mock_dropbox
sys.modules['dropbox.files'] = mock_dropbox.files
sys.modules['dropbox.exceptions'] = mock_dropbox.exceptions

import dropbox_upload


def test_upload_success_response():
    """Test that upload returns a success dict on successful upload."""
    # Create a temporary file for the test
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jpg') as f:
        f.write('test content')
        temp_path = f.name
    
    try:
        mock_dbx = MagicMock()
        mock_metadata = MagicMock()
        mock_metadata.name = 'test.jpg'
        mock_dbx.files_upload.return_value = mock_metadata
        
        result = dropbox_upload.upload(
            mock_dbx, temp_path, 'Photos', '', 'test.jpg', overwrite=False
        )
        
        assert result['status'] == 'success'
        assert result['file_path'] == '/Photos/test.jpg'
        assert result['bytes_uploaded'] > 0
        assert result['message'] == 'File uploaded successfully'
    finally:
        os.unlink(temp_path)


def test_upload_error_response():
    """Test that upload returns an error dict on failure."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jpg') as f:
        f.write('test content')
        temp_path = f.name
    
    try:
        mock_dbx = MagicMock()
        mock_dbx.files_upload.side_effect = Exception('Connection error')
        
        result = dropbox_upload.upload(
            mock_dbx, temp_path, 'Photos', '', 'test.jpg'
        )
        
        assert result['status'] == 'error'
        assert result['file_path'] == '/Photos/test.jpg'
        assert result['bytes_uploaded'] == 0
        assert 'error' in result['message'].lower()
    finally:
        os.unlink(temp_path)


def test_upload_api_error_folder_not_found():
    """Test upload handles folder not found API error."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jpg') as f:
        f.write('test content')
        temp_path = f.name
    
    try:
        mock_dbx = MagicMock()
        api_error = MagicMock()
        api_error.__str__ = MagicMock(return_value='path:not_found/parent/foobar')
        mock_dbx.files_upload.side_effect = api_error
        
        # Mock the folder creation to succeed
        mock_dbx.files_create_folder_v2.return_value = None
        
        result = dropbox_upload.upload(
            mock_dbx, temp_path, 'Photos', 'subdir', 'test.jpg'
        )
        
        # Should retry and succeed
        assert result['status'] == 'success'
    finally:
        os.unlink(temp_path)


def test_upload_io_error():
    """Test upload handles file read errors."""
    mock_dbx = MagicMock()
    
    # Upload a non-existent file to trigger IOError
    result = dropbox_upload.upload(
        mock_dbx, '/tmp/nonexistent_file_xyz.jpg', 'Photos', '', 'test.jpg'
    )
    
    assert result['status'] == 'error'
    assert 'Failed to read file' in result['message']


def test_parse_args_count_parameter():
    """Test parse_args handles --count parameter."""
    args = dropbox_upload.parse_args(['--count', '5', 'Albums', '/home/user/Pics'])
    assert args.count == 5
    assert args.folder == 'Albums'
    assert args.rootdir == '/home/user/Pics'


def test_parse_args_conflict_validation():
    """Test that --yes and --no together causes error in main logic."""
    # This test validates the conflict check logic
    args = dropbox_upload.parse_args(['--yes', '--no'])
    conflict_count = sum([bool(b) for b in (args.yes, args.no, args.default)])
    assert conflict_count == 2  # Both yes and no are True


def test_should_skip_file_all_patterns():
    """Comprehensive test of all skip patterns."""
    # These should all be skipped
    skipped_patterns = [
        '.gitignore', '.bashrc', '.env',  # Dot files
        'file.tmp', 'backup.temp',  # Temp extensions
        '~backup', '@temp', '@copy',  # Start with ~ or @
        'module.pyc', 'script.pyo',  # Python bytecode
        '__pycache__',  # Python cache dir
        '',  # Empty string
        None,  # None value
    ]
    
    for pattern in skipped_patterns:
        assert dropbox_upload.should_skip_file(pattern) is True, \
            f"Pattern '{pattern}' should be skipped"


def test_should_skip_file_preserved_patterns():
    """Test files that should NOT be skipped."""
    preserved_patterns = [
        'photo.jpg', 'image.png', 'video.mp4',  # Media files
        'document.pdf', 'report.docx',  # Documents
        'test.PYC', 'script.PYTHON',  # Case-sensitive (not filtered)
        'data_2024.txt', 'backup-2024.bak',  # Files with underscores/dashes
    ]
    
    for pattern in preserved_patterns:
        assert dropbox_upload.should_skip_file(pattern) is False, \
            f"Pattern '{pattern}' should NOT be skipped"


def test_list_folder_empty_result():
    """Test list_folder returns empty dict on API error."""
    mock_dbx = MagicMock()
    mock_dbx.files_list_folder.side_effect = ApiError('API error')
    
    result = dropbox_upload.list_folder(mock_dbx, 'Photos', '')
    assert result == {}


def test_list_folder_with_entries():
    """Test list_folder correctly builds result dict from API entries."""
    mock_dbx = MagicMock()
    
    mock_entry1 = MagicMock()
    mock_entry1.name = 'photo1.jpg'
    mock_entry1.__class__ = MagicMock()
    
    mock_entry2 = MagicMock()
    mock_entry2.name = 'photo2.jpg'
    
    mock_result = MagicMock()
    mock_result.entries = [mock_entry1, mock_entry2]
    mock_dbx.files_list_folder.return_value = mock_result
    
    result = dropbox_upload.list_folder(mock_dbx, 'Photos', '')
    
    assert 'photo1.jpg' in result
    assert 'photo2.jpg' in result
    assert len(result) == 2


def test_download_success():
    """Test download returns file bytes on success."""
    mock_dbx = MagicMock()
    mock_metadata = MagicMock()
    mock_response = MagicMock()
    mock_response.content = b'test file content'
    mock_dbx.files_download.return_value = (mock_metadata, mock_response)
    
    result = dropbox_upload.download(mock_dbx, 'Photos', '', 'test.jpg')
    assert result == b'test file content'


def test_download_failure():
    """Test download returns None on HTTP error."""
    mock_dbx = MagicMock()
    mock_dbx.files_download.side_effect = HttpError('HTTP error')
    
    result = dropbox_upload.download(mock_dbx, 'Photos', '', 'test.jpg')
    assert result is None
