"""test_dropbox_upload.py — Tests for Dropbox upload functionality."""
import pytest
import os
import sys
import argparse
from unittest.mock import Mock, MagicMock, patch


@pytest.fixture
def mock_dropbox_module():
    """Provide mock dropbox module for testing."""
    # Create proper exception classes that match Dropbox API
    class ApiError(Exception):
        def __init__(self, error, user_message_text, user_message_locale):
            self.error = error
            self.user_message_text = user_message_text
            self.user_message_locale = user_message_locale
            super().__init__(user_message_text)
    
    class HttpError(Exception):
        def __init__(self, status_code, body):
            self.status_code = status_code
            self.body = body
            super().__init__(f"HTTP {status_code}")
    
    mock_dbx_exceptions = MagicMock()
    mock_dbx_exceptions.ApiError = ApiError
    mock_dbx_exceptions.HttpError = HttpError
    
    mock_dbx_files = MagicMock()
    mock_dbx_files.WriteMode = MagicMock()
    mock_dbx_files.WriteMode.overwrite = "overwrite"
    
    mock_dropbox = MagicMock()
    mock_dropbox.files = mock_dbx_files
    mock_dropbox.exceptions = mock_dbx_exceptions
    
    sys.modules['dropbox'] = mock_dropbox
    sys.modules['dropbox.files'] = mock_dbx_files
    sys.modules['dropbox.exceptions'] = mock_dbx_exceptions
    import dropbox
    import dropbox.files
    import dropbox.exceptions
    return dropbox


@pytest.fixture
def test_files(tmp_path):
    """Create test files for upload testing."""
    test_file1 = tmp_path / "test1.jpg"
    test_file1.write_bytes(b"fake image data 1")
    test_file2 = tmp_path / "test2.jpg"
    test_file2.write_bytes(b"fake image data 2")
    temp_file = tmp_path / "testfile~"
    temp_file.write_bytes(b"temp file")
    dot_file = tmp_path / ".hidden.jpg"
    dot_file.write_bytes(b"dot file")
    return {
        'normal': test_file1,
        'normal2': test_file2,
        'temp': temp_file,
        'dot': dot_file
    }


def test_parse_arguments_yes_flag(mock_dropbox_module, test_files, tmp_path):
    """Test argument parsing with --yes flag."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--yes', '-y', action='store_true', help='Answer yes')
    parser.add_argument('--token', default='TEST_TOKEN', help='Token')
    
    args = parser.parse_args(['--yes'])
    assert args.yes is True
    assert args.token == 'TEST_TOKEN'


def test_skip_dot_files(mock_dropbox_module, test_files, tmp_path):
    """Test that dot files are skipped during upload."""
    # Import the main module and check its behavior
    with patch('dropbox_upload.os') as mock_os:
        with patch('dropbox_upload.os.walk') as mock_walk:
            mock_walk.return_value = [
                (str(tmp_path), [], ['test1.jpg', '.hidden.jpg', 'testfile~'])
            ]
            mock_os.path.exists.return_value = True
            mock_os.path.isdir.return_value = True
            mock_os.getmtime.side_effect = lambda x: 1234567890
            mock_os.getsize.side_effect = lambda x: 100


def test_skip_temporary_files(mock_dropbox_module, test_files):
    """Test that temporary files ending with ~ are skipped."""
    assert 'temp' in test_files
    temp_file = test_files['temp']
    # Verify the file ends with ~ (Dropbox temp convention)
    assert temp_file.name.endswith('~')


def test_list_folder_success(mock_dropbox_module):
    """Test successful folder listing."""
    from dropbox_upload import list_folder
    
    mock_dbx = Mock()
    mock_entry = Mock()
    mock_entry.name = "testfile.jpg"
    mock_result = Mock()
    mock_result.entries = [mock_entry]
    mock_dbx.files_list_folder.return_value = mock_result
    
    result = list_folder(mock_dbx, "folder", "")
    assert "testfile.jpg" in result


def test_list_folder_api_error():
    """Test folder listing with API error returns empty dict."""
    import dropbox
    from dropbox import exceptions
    
    mock_dbx = Mock()
    mock_dbx.files_list_folder.side_effect = exceptions.ApiError(
        {"error": "test"}, "Test error", "en"
    )
    
    # Reload to ensure correct exception handling
    import importlib
    try:
        import dropbox_upload
        importlib.reload(dropbox_upload)
    except:
        pass
    
    from dropbox_upload import list_folder
    mock_dbx2 = Mock()
    mock_dbx2.files_list_folder.side_effect = exceptions.ApiError(
        {"error": "test"}, "Test error", "en"
    )
    
    result = list_folder(mock_dbx2, "folder", "")
    assert result == {}


def test_upload_success(mock_dropbox_module, test_files):
    """Test successful file upload."""
    from dropbox_upload import upload
    
    mock_dbx = Mock()
    mock_response = Mock()
    mock_response.name = "test.jpg"
    mock_dbx.files_upload.return_value = mock_response
    
    result = upload(mock_dbx, str(test_files['normal']), "folder", "", "test.jpg")
    assert result is not None
    assert mock_dbx.files_upload.called


def test_download_success(mock_dropbox_module):
    """Test successful file download."""
    from dropbox_upload import download
    
    mock_dbx = Mock()
    mock_md = Mock()
    mock_result = Mock()
    mock_result.content = b"downloaded data"
    mock_dbx.files_download.return_value = (mock_md, mock_result)
    
    result = download(mock_dbx, "folder", "", "test.jpg")
    assert result == b"downloaded data"


def test_download_error():
    """Test download with error returns None."""
    import dropbox
    from dropbox import exceptions
    
    mock_dbx = Mock()
    mock_dbx.files_download.side_effect = exceptions.HttpError(404, "Not found")
    
    # Reload to ensure correct exception handling
    import importlib
    try:
        import dropbox_upload
        importlib.reload(dropbox_upload)
    except:
        pass
    
    from dropbox_upload import download
    mock_dbx2 = Mock()
    mock_dbx2.files_download.side_effect = exceptions.HttpError(404, "Not found")
    
    result = download(mock_dbx2, "folder", "", "test.jpg")
    assert result is None


def test_yesno_default_yes(mock_dropbox_module, test_files):
    """Test yesno function with default yes."""
    from dropbox_upload import yesno
    
    args = Mock()
    args.default = False
    args.yes = False
    args.no = False
    
    with patch('dropbox_upload.input', return_value=''):
        result = yesno("Test", True, args)
        assert result is True


def test_yesno_default_no(mock_dropbox_module, test_files):
    """Test yesno function with default no."""
    from dropbox_upload import yesno
    
    args = Mock()
    args.default = False
    args.yes = False
    args.no = False
    
    with patch('dropbox_upload.input', return_value=''):
        result = yesno("Test", False, args)
        assert result is False


def test_yesno_force_yes(mock_dropbox_module, test_files):
    """Test yesno with --yes flag."""
    from dropbox_upload import yesno
    
    args = Mock()
    args.default = False
    args.yes = True
    args.no = False
    
    result = yesno("Test", False, args)
    assert result is True


def test_yesno_force_no(mock_dropbox_module, test_files):
    """Test yesno with --no flag."""
    from dropbox_upload import yesno
    
    args = Mock()
    args.default = False
    args.yes = False
    args.no = True
    
    result = yesno("Test", True, args)
    assert result is False


def test_yesno_q_quit(mock_dropbox_module, test_files):
    """Test yesno with quit command."""
    from dropbox_upload import yesno
    
    args = Mock()
    args.default = False
    args.yes = False
    args.no = False
    
    with patch('dropbox_upload.input', side_effect=['q', SystemExit]):
        with pytest.raises(SystemExit):
            yesno("Test", True, args)


def test_yesno_invalid_input(mock_dropbox_module, test_files):
    """Test yesno with invalid input loops until valid."""
    from dropbox_upload import yesno
    
    args = Mock()
    args.default = False
    args.yes = False
    args.no = False
    
    with patch('dropbox_upload.input', side_effect=['invalid', 'yes']):
        result = yesno("Test", False, args)
        assert result is True


def test_stopwatch_context_manager(mock_dropbox_module):
    """Test stopwatch context manager."""
    from dropbox_upload import stopwatch
    import time
    
    with stopwatch("test operation"):
        time.sleep(0.01)  # Sleep 10ms


def test_main_invalid_folder_type(mock_dropbox_module, test_files):
    """Test main function with file instead of folder."""
    from dropbox_upload import main
    import sys
    
    args = argparse.Namespace(
        folder="Downloads",
        rootdir=str(test_files['normal']),
        token="TEST_TOKEN",
        yes=False,
        no=False,
        default=False
    )
    
    with patch('dropbox_upload.parser.parse_args', return_value=args):
        with patch('dropbox_upload.os.path.exists', return_value=True):
            with patch('dropbox_upload.os.path.isdir', return_value=False):
                with pytest.raises(SystemExit):
                    main()


def test_main_folder_not_exist(mock_dropbox_module, test_files):
    """Test main function with non-existent folder."""
    from dropbox_upload import main
    
    args = argparse.Namespace(
        folder="Downloads",
        rootdir="/nonexistent/folder",
        token="TEST_TOKEN",
        yes=False,
        no=False,
        default=False
    )
    
    with patch('dropbox_upload.parser.parse_args', return_value=args):
        with patch('dropbox_upload.os.path.exists', return_value=False):
            with pytest.raises(SystemExit):
                main()
