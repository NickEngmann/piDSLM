"""Tests for dropbox_upload.py - Dropbox upload functionality"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open

# Add the repo directory to the path
sys.path.insert(0, '')


def test_parse_arguments():
    """Test argument parsing"""
    import dropbox_upload
    
    # Test that parser is defined
    assert hasattr(dropbox_upload, 'parser')
    assert dropbox_upload.parser is not None


def test_list_folder_success():
    """Test list_folder function"""
    with patch('dropbox_upload.dropbox') as mock_db_module:
        mock_dbx = MagicMock()
        mock_entry1 = MagicMock()
        mock_entry1.name = 'file1.txt'
        mock_entry2 = MagicMock()
        mock_entry2.name = 'file2.txt'
        mock_response = MagicMock()
        mock_response.entries = [mock_entry1, mock_entry2]
        mock_dbx.files_list_folder.return_value = mock_response
        
        import dropbox_upload
        
        result = dropbox_upload.list_folder(mock_dbx, 'folder', 'subfolder')
        
        assert 'file1.txt' in result
        assert 'file2.txt' in result


def test_list_folder_api_error():
    """Test list_folder with API error"""
    with patch('dropbox_upload.dropbox') as mock_db_module:
        mock_dbx = MagicMock()
        mock_dbx.files_list_folder.side_effect = Exception('ApiError')
        
        import dropbox_upload
        
        result = dropbox_upload.list_folder(mock_dbx, 'folder', 'subfolder')
        
        # Should return empty dict on error
        assert result == {}


def test_download_success():
    """Test download function"""
    with patch('dropbox_upload.dropbox') as mock_db_module:
        mock_dbx = MagicMock()
        mock_metadata = MagicMock()
        mock_response = MagicMock()
        mock_response.content = b'test data'
        mock_dbx.files_download.return_value = (mock_metadata, mock_response)
        
        import dropbox_upload
        
        result = dropbox_upload.download(mock_dbx, 'folder', 'subfolder', 'file.txt')
        
        assert result == b'test data'


def test_download_http_error():
    """Test download with HTTP error"""
    with patch('dropbox_upload.dropbox') as mock_db_module:
        mock_dbx = MagicMock()
        mock_dbx.files_download.side_effect = Exception('HttpError')
        
        import dropbox_upload
        
        result = dropbox_upload.download(mock_dbx, 'folder', 'subfolder', 'file.txt')
        
        assert result is None


def test_upload_success():
    """Test upload function"""
    with patch('dropbox_upload.dropbox') as mock_db_module, \
         patch('dropbox_upload.os.path.exists') as mock_exists, \
         patch('dropbox_upload.os.path.getmtime') as mock_mtime, \
         patch('dropbox_upload.os.path.getsize') as mock_size, \
         patch('dropbox_upload.open', mock_open(read_data=b'test data')):
        
        mock_dbx = MagicMock()
        mock_response = MagicMock()
        mock_response.name = 'uploaded.txt'
        mock_dbx.files_upload.return_value = mock_response
        
        mock_exists.return_value = True
        mock_mtime.return_value = 0
        mock_size.return_value = 100
        
        import dropbox_upload
        
        result = dropbox_upload.upload(mock_dbx, 'test_file.txt', 'folder', 'subfolder', 'file.txt')
        
        assert result is not None
        assert mock_dbx.files_upload.called


def test_yesno_with_yes_argument():
    """Test yesno function with --yes argument"""
    import dropbox_upload
    
    # Create mock args with yes=True
    mock_args = MagicMock()
    mock_args.yes = True
    mock_args.no = False
    mock_args.default = False
    
    result = dropbox_upload.yesno('Test question', False, mock_args)
    
    assert result is True


def test_yesno_with_no_argument():
    """Test yesno function with --no argument"""
    import dropbox_upload
    
    mock_args = MagicMock()
    mock_args.yes = False
    mock_args.no = True
    mock_args.default = False
    
    result = dropbox_upload.yesno('Test question', True, mock_args)
    
    assert result is False


def test_yesno_with_default_argument():
    """Test yesno function with --default argument"""
    import dropbox_upload
    
    mock_args = MagicMock()
    mock_args.yes = False
    mock_args.no = False
    mock_args.default = True
    
    result = dropbox_upload.yesno('Test question', True, mock_args)
    
    assert result is True


def test_elapsed_time_context_manager():
    """Test the stopwatch context manager"""
    with patch('dropbox_upload.time') as mock_time:
        mock_time.time.side_effect = [0, 1.5]
        
        import dropbox_upload
        
        # Test context manager
        with dropbox_upload.stopwatch('test operation'):
            pass
        
        # Verify time was called
        assert mock_time.time.called


def test_main_with_token():
    """Test main function with access token"""
    with patch('dropbox_upload.parser.parse_args') as mock_parse, \
         patch('dropbox_upload.dropbox.Dropbox') as mock_dropbox_class, \
         patch('dropbox_upload.os.path.exists') as mock_exists, \
         patch('dropbox_upload.os.path.isdir') as mock_isdir, \
         patch('dropbox_upload.os.walk') as mock_walk, \
         patch('dropbox_upload.os.path.join') as mock_join, \
         patch('dropbox_upload.os.path.getmtime') as mock_mtime, \
         patch('dropbox_upload.os.path.getsize') as mock_size, \
         patch('dropbox_upload.os.listdir') as mock_listdir, \
         patch('dropbox_upload.input', return_value=''), \
         patch('dropbox_upload.sys.exit') as mock_exit:
        
        # Mock arguments
        mock_args = MagicMock()
        mock_args.token = 'test_token'
        mock_args.folder = 'Downloads'
        mock_args.rootdir = '/test'
        mock_args.yes = False
        mock_args.no = False
        mock_args.default = False
        mock_parse.return_value = mock_args
        
        # Mock file system
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test', [], ['file1.txt'])
        ]
        mock_join.side_effect = lambda *args: '/'.join(args)
        mock_mtime.return_value = 0
        mock_size.return_value = 100
        mock_listdir.return_value = []
        
        # Mock Dropbox client
        mock_dbx_instance = MagicMock()
        mock_dropbox_class.return_value = mock_dbx_instance
        
        import dropbox_upload
        
        # Test main function
        try:
            dropbox_upload.main()
        except SystemExit:
            pass
        
        # Verify Dropbox client was created
        assert mock_dropbox_class.called
        assert mock_parse.called


def test_main_with_missing_directory():
    """Test main function with non-existent directory"""
    with patch('dropbox_upload.parser.parse_args') as mock_parse, \
         patch('dropbox_upload.os.path.exists') as mock_exists, \
         patch('dropbox_upload.sys.exit') as mock_exit:
        
        mock_args = MagicMock()
        mock_args.token = 'test_token'
        mock_args.folder = 'Downloads'
        mock_args.rootdir = '/nonexistent'
        mock_args.yes = False
        mock_args.no = False
        mock_args.default = False
        mock_parse.return_value = mock_args
        
        mock_exists.return_value = False
        
        import dropbox_upload
        
        try:
            dropbox_upload.main()
        except SystemExit:
            pass
        
        assert mock_exit.called


def test_main_with_non_directory():
    """Test main function with file instead of directory"""
    with patch('dropbox_upload.parser.parse_args') as mock_parse, \
         patch('dropbox_upload.os.path.exists') as mock_exists, \
         patch('dropbox_upload.os.path.isdir') as mock_isdir, \
         patch('dropbox_upload.sys.exit') as mock_exit:
        
        mock_args = MagicMock()
        mock_args.token = 'test_token'
        mock_args.folder = 'Downloads'
        mock_args.rootdir = '/test/file.txt'
        mock_args.yes = False
        mock_args.no = False
        mock_args.default = False
        mock_parse.return_value = mock_args
        
        mock_exists.return_value = True
        mock_isdir.return_value = False
        
        import dropbox_upload
        
        try:
            dropbox_upload.main()
        except SystemExit:
            pass
        
        assert mock_exit.called
