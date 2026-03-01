"""Tests for dropbox_upload.py functionality."""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock, call
from io import StringIO

# Add the repo directory to the path
sys.path.insert(0, '')


def test_dropbox_parser_defaults():
    """Test that the argument parser has correct defaults."""
    with patch('dropbox_upload.parser') as mock_parser:
        # Import the module to get the parser
        import dropbox_upload
        
        # Test default values
        args = dropbox_upload.parser.parse_args([])
        assert args.folder == 'Downloads'
        assert args.rootdir == '~/Downloads'
        assert args.token == 'YOUR_ACCESS_TOKEN'
        assert args.yes is False
        assert args.no is False
        assert args.default is False


def test_dropbox_parser_custom_args():
    """Test argument parser with custom values."""
    import dropbox_upload
    
    args = dropbox_upload.parser.parse_args([
        '--folder', 'TestFolder',
        '--rootdir', '/home/user/test',
        '--token', 'test_token_123',
        '--yes'
    ])
    
    assert args.folder == 'TestFolder'
    assert args.rootdir == '/home/user/test'
    assert args.token == 'test_token_123'
    assert args.yes is True


def test_dropbox_yesno_with_yes_flag():
    """Test yesno function with --yes flag."""
    import dropbox_upload
    
    # Mock args with yes flag
    args = MagicMock()
    args.yes = True
    args.no = False
    args.default = False
    
    # Should return True regardless of question
    result = dropbox_upload.yesno('Test question', False, args)
    assert result is True


def test_dropbox_yesno_with_no_flag():
    """Test yesno function with --no flag."""
    import dropbox_upload
    
    args = MagicMock()
    args.yes = False
    args.no = True
    args.default = False
    
    result = dropbox_upload.yesno('Test question', True, args)
    assert result is False


def test_dropbox_yesno_with_default_flag():
    """Test yesno function with --default flag."""
    import dropbox_upload
    
    args = MagicMock()
    args.yes = False
    args.no = False
    args.default = True
    
    result = dropbox_upload.yesno('Test question', True, args)
    assert result is True
    
    result = dropbox_upload.yesno('Test question 2', False, args)
    assert result is False


def test_dropbox_yesno_user_yes():
    """Test yesno function with user input 'yes'."""
    import dropbox_upload
    
    args = MagicMock()
    args.yes = False
    args.no = False
    args.default = False
    
    with patch('dropbox_upload.input', return_value='yes'):
        result = dropbox_upload.yesno('Test question', False, args)
        assert result is True


def test_dropbox_yesno_user_y():
    """Test yesno function with user input 'y'."""
    import dropbox_upload
    
    args = MagicMock()
    args.yes = False
    args.no = False
    args.default = False
    
    with patch('dropbox_upload.input', return_value='y'):
        result = dropbox_upload.yesno('Test question', False, args)
        assert result is True


def test_dropbox_yesno_user_no():
    """Test yesno function with user input 'no'."""
    import dropbox_upload
    
    args = MagicMock()
    args.yes = False
    args.no = False
    args.default = False
    
    with patch('dropbox_upload.input', return_value='no'):
        result = dropbox_upload.yesno('Test question', True, args)
        assert result is False


def test_dropbox_yesno_default_answer():
    """Test yesno function with default answer (empty input)."""
    import dropbox_upload
    
    args = MagicMock()
    args.yes = False
    args.no = False
    args.default = False
    
    # When default is True, empty input should return True
    with patch('dropbox_upload.input', return_value=''):
        result = dropbox_upload.yesno('Test question', True, args)
        assert result is True
    
    # When default is False, empty input should return False
    with patch('dropbox_upload.input', return_value=''):
        result = dropbox_upload.yesno('Test question', False, args)
        assert result is False


def test_list_folder_success():
    """Test list_folder function with successful API call."""
    import dropbox_upload
    
    mock_dbx = MagicMock()
    mock_response = MagicMock()
    mock_entry1 = MagicMock()
    mock_entry1.name = 'file1.txt'
    mock_entry2 = MagicMock()
    mock_entry2.name = 'file2.txt'
    mock_response.entries = [mock_entry1, mock_entry2]
    mock_dbx.files_list_folder.return_value = mock_response
    
    result = dropbox_upload.list_folder(mock_dbx, 'TestFolder', 'subfolder')
    
    assert 'file1.txt' in result
    assert 'file2.txt' in result
    mock_dbx.files_list_folder.assert_called_once()


def test_list_folder_empty():
    """Test list_folder function with empty folder."""
    import dropbox_upload
    
    mock_dbx = MagicMock()
    mock_response = MagicMock()
    mock_response.entries = []
    mock_dbx.files_list_folder.return_value = mock_response
    
    result = dropbox_upload.list_folder(mock_dbx, 'TestFolder', '')
    
    assert result == {}


def test_list_folder_api_error():
    """Test list_folder function with API error."""
    import dropbox_upload
    
    mock_dbx = MagicMock()
    mock_dbx.files_list_folder.side_effect = Exception('API Error')
    
    result = dropbox_upload.list_folder(mock_dbx, 'TestFolder', '')
    
    # Should return empty dict on error
    assert result == {}


def test_download_file_success():
    """Test download function with successful download."""
    import dropbox_upload
    
    mock_dbx = MagicMock()
    mock_md = MagicMock()
    mock_response = MagicMock()
    mock_response.content = b'file content here'
    mock_dbx.files_download.return_value = (mock_md, mock_response)
    
    result = dropbox_upload.download(mock_dbx, 'TestFolder', 'subfolder', 'file.txt')
    
    assert result == b'file content here'
    mock_dbx.files_download.assert_called_once()


def test_download_file_not_found():
    """Test download function with file not found."""
    import dropbox_upload
    
    mock_dbx = MagicMock()
    mock_dbx.files_download.side_effect = Exception('HTTP Error 404')
    
    result = dropbox_upload.download(mock_dbx, 'TestFolder', 'subfolder', 'file.txt')
    
    assert result is None


def test_upload_file_success():
    """Test upload function with successful upload."""
    import dropbox_upload
    
    mock_dbx = MagicMock()
    mock_response = MagicMock()
    mock_response.name = 'uploaded_file.txt'
    mock_dbx.files_upload.return_value = mock_response
    
    # Create a temporary test file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write('test content')
        temp_file = f.name
    
    try:
        result = dropbox_upload.upload(mock_dbx, temp_file, 'TestFolder', 'subfolder', 'file.txt')
        
        assert result is not None
        mock_dbx.files_upload.assert_called_once()
    finally:
        os.unlink(temp_file)


def test_upload_file_overwrite():
    """Test upload function with overwrite mode."""
    import dropbox_upload
    
    mock_dbx = MagicMock()
    mock_response = MagicMock()
    mock_dbx.files_upload.return_value = mock_response
    
    # Create a temporary test file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write('test content')
        temp_file = f.name
    
    try:
        result = dropbox_upload.upload(mock_dbx, temp_file, 'TestFolder', 'subfolder', 'file.txt', overwrite=True)
        
        assert result is not None
        # Verify overwrite mode was used
        call_kwargs = mock_dbx.files_upload.call_args[1]
        assert 'mode' in call_kwargs
    finally:
        os.unlink(temp_file)


def test_stopwatch_context_manager():
    """Test the stopwatch context manager."""
    import dropbox_upload
    import time
    
    # Mock time.time to control timing
    with patch('dropbox_upload.time.time') as mock_time:
        mock_time.side_effect = [0, 1.5]  # Start at 0, end at 1.5 seconds
        
        output = []
        with patch('builtins.print', side_effect=lambda *args: output.append(args)):
            with dropbox_upload.stopwatch('test operation'):
                pass
        
        # Verify elapsed time was printed
        assert len(output) >= 1
        output_str = ' '.join(str(item) for item in output[0])
        assert 'elapsed' in output_str.lower() or '1.5' in output_str


def test_main_with_invalid_args():
    """Test main function with invalid argument combinations."""
    import dropbox_upload
    
    # Test with both --yes and --no (should exit)
    with patch('sys.argv', ['dropbox_upload.py', '--yes', '--no']):
        with patch('sys.exit') as mock_exit:
            try:
                dropbox_upload.main()
            except SystemExit:
                pass
            mock_exit.assert_called_once()


def test_main_with_missing_token():
    """Test main function with missing token."""
    import dropbox_upload
    
    # Test with no token provided
    with patch('sys.argv', ['dropbox_upload.py']):
        with patch('sys.exit') as mock_exit:
            try:
                dropbox_upload.main()
            except SystemExit:
                pass
            mock_exit.assert_called_once()


def test_main_with_nonexistent_directory():
    """Test main function with non-existent directory."""
    import dropbox_upload
    
    with patch('sys.argv', ['dropbox_upload.py', '--rootdir', '/nonexistent/path', '--token', 'test']):
        with patch('sys.exit') as mock_exit:
            try:
                dropbox_upload.main()
            except SystemExit:
                pass
            mock_exit.assert_called_once()


def test_main_with_file_upload():
    """Test main function with actual file upload simulation."""
    import dropbox_upload
    
    # Create a temporary directory with a test file
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, 'test.txt')
    with open(test_file, 'w') as f:
        f.write('test content')
    
    try:
        mock_dbx = MagicMock()
        mock_dbx.files_list_folder.return_value = MagicMock()
        mock_dbx.files_list_folder.return_value.entries = []
        
        with patch('dropbox.Dropbox', return_value=mock_dbx):
            with patch('sys.argv', ['dropbox_upload.py', '--rootdir', temp_dir, '--token', 'test', '--yes']):
                with patch('builtins.print'):
                    try:
                        dropbox_upload.main()
                    except SystemExit:
                        pass
                    
                    # Should have attempted to list folder
                    mock_dbx.files_list_folder.assert_called()
    finally:
        shutil.rmtree(temp_dir)
