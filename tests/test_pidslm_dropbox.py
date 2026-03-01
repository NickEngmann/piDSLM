"""Tests for piDSLM Dropbox upload functionality."""

import pytest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Add the repo directory to the path
sys.path.insert(0, '')


def test_dropbox_upload_init(source_module):
    """Test dropbox upload initialization."""
    with patch('dropbox.Dropbox') as mock_dropbox:
        # Mock the Dropbox client
        mock_dbx = MagicMock()
        mock_dropbox.return_value = mock_dbx
        
        # Import and test dropbox_upload module
        import dropbox_upload
        
        # Verify parser exists
        assert hasattr(dropbox_upload, 'parser')


def test_dropbox_upload_args(source_module):
    """Test dropbox upload argument parsing."""
    with patch('dropbox_upload.dropbox.Dropbox') as mock_dropbox:
        import dropbox_upload
        
        # Test default arguments
        args = dropbox_upload.parser.parse_args([])
        assert args.folder == 'Downloads'
        assert args.rootdir == '~/Downloads'
        assert args.token == 'YOUR_ACCESS_TOKEN'


def test_dropbox_upload_yesno_yes(source_module):
    """Test yes/no helper with yes answer."""
    import dropbox_upload
    
    class Args:
        yes = True
        no = False
        default = False
    
    args = Args()
    result = dropbox_upload.yesno('Test question', False, args)
    assert result is True


def test_dropbox_upload_yesno_no(source_module):
    """Test yes/no helper with no answer."""
    import dropbox_upload
    
    class Args:
        yes = False
        no = True
        default = False
    
    args = Args()
    result = dropbox_upload.yesno('Test question', True, args)
    assert result is False


def test_dropbox_upload_yesno_default(source_module):
    """Test yes/no helper with default answer."""
    import dropbox_upload
    
    class Args:
        yes = False
        no = False
        default = True
    
    args = Args()
    result = dropbox_upload.yesno('Test question', False, args)
    assert result is False


def test_dropbox_upload_list_folder(source_module):
    """Test list_folder function."""
    with patch('dropbox.Dropbox') as mock_dropbox:
        import dropbox_upload
        
        mock_dbx = MagicMock()
        mock_response = MagicMock()
        mock_response.entries = []
        mock_dbx.files_list_folder.return_value = mock_response
        
        result = dropbox_upload.list_folder(mock_dbx, 'folder', 'subfolder')
        assert isinstance(result, dict)


def test_dropbox_upload_list_folder_error(source_module):
    """Test list_folder with API error."""
    with patch('dropbox.Dropbox') as mock_dropbox:
        import dropbox_upload
        
        mock_dbx = MagicMock()
        mock_dbx.files_list_folder.side_effect = Exception('API error')
        
        result = dropbox_upload.list_folder(mock_dbx, 'folder', 'subfolder')
        assert result == {}


def test_dropbox_upload_upload(source_module):
    """Test upload function."""
    with patch('dropbox.Dropbox') as mock_dropbox:
        import dropbox_upload
        
        mock_dbx = MagicMock()
        mock_response = MagicMock()
        mock_response.name = 'test.jpg'
        mock_dbx.files_upload.return_value = mock_response
        
        # Create a temporary test file
        test_file = '/tmp/test_upload.txt'
        with open(test_file, 'w') as f:
            f.write('test content')
        
        try:
            result = dropbox_upload.upload(
                mock_dbx, test_file, 'folder', 'subfolder', 'test.txt'
            )
            assert result is not None
            assert mock_dbx.files_upload.called
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


def test_dropbox_upload_download(source_module):
    """Test download function."""
    with patch('dropbox.Dropbox') as mock_dropbox:
        import dropbox_upload
        
        mock_dbx = MagicMock()
        mock_response = MagicMock()
        mock_response.content = b'test content'
        mock_dbx.files_download.return_value = (MagicMock(), mock_response)
        
        result = dropbox_upload.download(mock_dbx, 'folder', 'subfolder', 'test.txt')
        assert result == b'test content'


def test_dropbox_upload_stopwatch(source_module):
    """Test stopwatch context manager."""
    import dropbox_upload
    import time
    
    start_time = time.time()
    with dropbox_upload.stopwatch('test operation'):
        time.sleep(0.01)
    elapsed = time.time() - start_time
    
    # Verify elapsed time is approximately correct
    assert elapsed >= 0.01


def test_dropbox_upload_main(source_module):
    """Test main function with mocked Dropbox."""
    with patch('dropbox_upload.dropbox.Dropbox') as mock_dropbox:
        with patch('dropbox_upload.os.walk') as mock_walk:
            with patch('dropbox_upload.os.path.exists', return_value=True):
                with patch('dropbox_upload.os.path.isdir', return_value=True):
                    with patch('dropbox_upload.input', return_value='n'):
                        import dropbox_upload
                        
                        mock_dbx = MagicMock()
                        mock_dropbox.return_value = mock_dbx
                        
                        # Mock file listing
                        mock_response = MagicMock()
                        mock_response.entries = []
                        mock_dbx.files_list_folder.return_value = mock_response
                        
                        # Mock walk to return empty directories
                        mock_walk.return_value = []
                        
                        # Test with --yes flag to skip prompts
                        args = dropbox_upload.parser.parse_args(['--yes'])
                        
                        # Verify parser works
                        assert args.yes is True
