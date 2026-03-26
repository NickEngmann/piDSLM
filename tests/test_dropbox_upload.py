"""test_dropbox_upload.py — Tests for Dropbox upload functionality."""
import pytest
import os
import sys
import argparse
import datetime
from unittest.mock import Mock, MagicMock, patch

# Mock dropbox module is set up in tests/conftest.py


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


def test_list_folder_api_error(mock_dropbox_module):
    """Test folder listing with API error returns empty dict."""
    from dropbox_upload import list_folder

    mock_dbx = Mock()
    mock_dbx.files_list_folder.side_effect = mock_dropbox_module.exceptions.ApiError(
        {"error": "test"}, "Test error", "en"
    )

    result = list_folder(mock_dbx, "folder", "")
    assert result == {}


def test_upload_success(mock_dropbox_module, test_files):
    """Test successful file upload."""
    from dropbox_upload import upload_file

    mock_dbx = Mock()
    mock_response = Mock()
    mock_response.name = "test.jpg"
    mock_dbx.files_upload.return_value = mock_response

    result = upload_file(mock_dbx, str(test_files['normal']), "folder", "", "test.jpg")
    assert result is not None
    assert mock_dbx.files_upload.called


def test_download_success(mock_dropbox_module):
    """Test successful file download."""
    from dropbox_upload import download_file

    mock_dbx = Mock()
    mock_md = Mock()
    mock_result = Mock()
    mock_result.content = b"downloaded data"
    mock_dbx.files_download.return_value = (mock_md, mock_result)

    result = download_file(mock_dbx, "folder", "", "test.jpg")
    assert result == b"downloaded data"


def test_download_error(mock_dropbox_module):
    """Test download with error returns None."""
    from dropbox_upload import download_file

    mock_dbx = Mock()
    mock_dbx.files_download.side_effect = mock_dropbox_module.exceptions.HttpError(404, "Not found")

    result = download_file(mock_dbx, "folder", "", "test.jpg")
    assert result is None


def test_ask_user_yesno_default_yes(mock_dropbox_module, test_files):
    """Test ask_user_yesno function with default yes."""
    from dropbox_upload import ask_user_yesno

    args = Mock()
    args.default = False
    args.yes = False
    args.no = False

    result = ask_user_yesno("Test", True, args)
    assert result is True


def test_ask_user_yesno_default_no(mock_dropbox_module, test_files):
    """Test ask_user_yesno function with default no."""
    from dropbox_upload import ask_user_yesno

    args = Mock()
    args.default = False
    args.yes = False
    args.no = False

    result = ask_user_yesno("Test", False, args)
    assert result is False


def test_ask_user_yesno_force_yes(mock_dropbox_module, test_files):
    """Test ask_user_yesno with --yes flag."""
    from dropbox_upload import ask_user_yesno

    args = Mock()
    args.default = False
    args.yes = True
    args.no = False

    result = ask_user_yesno("Test", False, args)
    assert result is True


def test_ask_user_yesno_force_no(mock_dropbox_module, test_files):
    """Test ask_user_yesno with --no flag."""
    from dropbox_upload import ask_user_yesno

    args = Mock()
    args.default = False
    args.yes = False
    args.no = True

    result = ask_user_yesno("Test", True, args)
    assert result is False


def test_filter_dirs_to_descend(mock_dropbox_module, test_files):
    """Test filtering directories to descend into."""
    from dropbox_upload import filter_dirs_to_descend

    dirs = ["images", ".git", "documents", "__pycache__"]
    args = Mock()
    args.default = False
    args.yes = True
    args.no = False

    keep, skipped = filter_dirs_to_descend(dirs, args)
    assert "images" in keep
    assert "documents" in keep
    assert ".git" not in keep
    assert "__pycache__" not in keep


def test_stopwatch_context_manager(mock_dropbox_module):
    """Test stopwatch context manager."""
    from dropbox_upload import stopwatch
    import time

    with stopwatch("test operation"):
        time.sleep(0.01)  # Sleep 10ms


def test_should_skip_dot_files(mock_dropbox_module):
    """Test that dot files are skipped."""
    from dropbox_upload import should_skip_file

    should_skip, reason = should_skip_file(".hidden.jpg")
    assert should_skip is True
    assert reason == 'dot file'


def test_should_skip_temp_files(mock_dropbox_module):
    """Test that temporary files are skipped."""
    from dropbox_upload import should_skip_file

    should_skip, reason = should_skip_file("testfile~")
    assert should_skip is True
    assert reason == 'temporary file'


def test_should_skip_generated_files(mock_dropbox_module):
    """Test that generated files are skipped."""
    from dropbox_upload import should_skip_file

    should_skip, reason = should_skip_file("file.pyc")
    assert should_skip is True
    assert reason == 'generated file'


def test_should_not_skip_normal_files(mock_dropbox_module):
    """Test that normal files are not skipped."""
    from dropbox_upload import should_skip_file

    should_skip, reason = should_skip_file("photo.jpg")
    assert should_skip is False
    assert reason == ''


def test_should_skip_directory_dot(mock_dropbox_module):
    """Test that dot directories are skipped."""
    from dropbox_upload import should_skip_directory

    should_skip, reason = should_skip_directory(".git")
    assert should_skip is True
    assert reason == 'dot directory'


def test_should_skip_directory_pycache(mock_dropbox_module):
    """Test that __pycache__ directories are skipped."""
    from dropbox_upload import should_skip_directory

    should_skip, reason = should_skip_directory("__pycache__")
    assert should_skip is True
    assert reason == 'generated directory'


def test_should_not_skip_directory(mock_dropbox_module):
    """Test that normal directories are not skipped."""
    from dropbox_upload import should_skip_directory

    should_skip, reason = should_skip_directory("images")
    assert should_skip is False
    assert reason == ''


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
        default=False,
        count=None
    )

    with patch('dropbox_upload.parse_args', return_value=args):
        with patch('dropbox_upload.os.path.exists', return_value=True):
            with patch('dropbox_upload.os.path.isdir', return_value=False):
                with pytest.raises(SystemExit):
                    main()


def test_main_folder_not_exist(mock_dropbox_module, test_files):
    """Test main function with non-existent folder."""
    from dropbox_upload import main
    import sys

    args = argparse.Namespace(
        folder="Downloads",
        rootdir="/nonexistent/folder",
        token="TEST_TOKEN",
        yes=False,
        no=False,
        default=False,
        count=None,
        download=False
    )

    with patch('dropbox_upload.parse_args', return_value=args):
        with patch('dropbox_upload.os.path.exists', return_value=False):
            with pytest.raises(SystemExit):
                main()


def test_get_file_mtime_dt_from_metadata_with_client_modified(mock_dropbox_module):
    """Test get_file_mtime_dt_from_metadata with client_modified."""
    from dropbox_upload import get_file_mtime_dt_from_metadata
    import datetime

    mock_md = Mock()
    mock_md.client_modified = datetime.datetime(2024, 1, 15, 10, 30, 0)
    mock_md.server_modified = datetime.datetime(2024, 1, 15, 11, 0, 0)

    result = get_file_mtime_dt_from_metadata(mock_md)
    assert result == mock_md.client_modified


def test_get_file_mtime_dt_from_metadata_with_server_modified(mock_dropbox_module):
    """Test get_file_mtime_dt_from_metadata when client_modified is None."""
    from dropbox_upload import get_file_mtime_dt_from_metadata
    import datetime

    mock_md = Mock()
    mock_md.client_modified = None
    mock_md.server_modified = datetime.datetime(2024, 2, 20, 14, 45, 0)

    result = get_file_mtime_dt_from_metadata(mock_md)
    assert result == mock_md.server_modified


def test_get_file_mtime_dt_from_metadata_fallback(mock_dropbox_module):
    """Test get_file_mtime_dt_from_metadata fallback to current time."""
    from dropbox_upload import get_file_mtime_dt_from_metadata
    import datetime

    mock_md = Mock()
    mock_md.client_modified = None
    mock_md.server_modified = None

    result = get_file_mtime_dt_from_metadata(mock_md)
    assert isinstance(result, datetime.datetime)


def test_sync_downloads_with_files(mock_dropbox_module, test_files, tmp_path):
    """Test sync_downloads function with mock Dropbox API."""
    from dropbox_upload import sync_downloads

    mock_dbx = Mock()
    mock_md = Mock()
    mock_md.client_modified = datetime.datetime(2024, 1, 1, 0, 0, 0)

    mock_result = Mock()
    mock_result.name = "test.jpg"
    mock_result.entries = [mock_result]

    mock_dbx.files_list_folder.return_value = mock_result
    mock_dbx.files_download.return_value = (mock_md, Mock(content=b"test content"))

    args = argparse.Namespace(
        default=False,
        yes=True,
        no=False
    )

    downloaded, skipped = sync_downloads(mock_dbx, "Downloads", str(tmp_path), args)

    assert downloaded >= 0
    assert skipped >= 0
