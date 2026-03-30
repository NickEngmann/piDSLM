"""Tests for dropbox_upload.py module.

Tests the modular functions: should_skip_file, should_skip_directory,
list_folder, download, upload, and yesno.

This test file imports the module directly using importlib to avoid issues
with the source_module fixture and while-True loop stripping.
"""
import pytest
import sys
import types
from unittest.mock import MagicMock, patch, Mock
import os
import tempfile
import datetime
import time

# Create the dropbox mock module first
_sys_dropbox = types.ModuleType('dropbox')

# Simple WriteMode class
class _WriteMode:
    add = 'add'
    overwrite = 'overwrite'

_sys_dropbox.files = types.ModuleType('dropbox.files')
_sys_dropbox.files.WriteMode = _WriteMode

class ApiError(Exception):
    def __init__(self, error, user_message_text, user_message_locale):
        self.error = error
        self.user_message_text = user_message_text
        self.user_message_locale = user_message_locale
        super().__init__(user_message_text)

class HttpError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

_sys_dropbox.exceptions = types.ModuleType('dropbox.exceptions')
_sys_dropbox.exceptions.ApiError = ApiError
_sys_dropbox.exceptions.HttpError = HttpError

_sys_dropbox.exceptions.ApiError = ApiError
_sys_dropbox.exceptions.HttpError = HttpError
sys.modules['dropbox'] = _sys_dropbox
sys.modules['dropbox.files'] = _sys_dropbox.files
sys.modules['dropbox.exceptions'] = _sys_dropbox.exceptions

# Now import the module we're testing
import importlib.util
spec = importlib.util.spec_from_file_location("dropbox_upload", 
    "/mnt/sandbox-ssd/workspaces/nickengmann-pidslm/repo/dropbox_upload.py")
dbu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dbu)
sys.modules['dropbox_upload'] = dbu


class TestShouldSkipFile:
    """Tests for should_skip_file function."""

    def test_skip_hidden_files(self):
        """Test that hidden files (starting with .) are skipped."""
        assert dbu.should_skip_file('.gitignore') is True
        assert dbu.should_skip_file('.bashrc') is True
        assert dbu.should_skip_file('.config') is True

    def test_skip_temp_files_tilde_end(self):
        """Test that files ending with ~ are skipped."""
        assert dbu.should_skip_file('file.txt~') is True
        assert dbu.should_skip_file('document~') is True

    def test_skip_temp_files_tilde_start(self):
        """Test that files starting with ~ are skipped."""
        assert dbu.should_skip_file('~file.txt') is True
        assert dbu.should_skip_file('~backup') is True

    def test_skip_temp_files_at_start(self):
        """Test that files starting with @ are skipped."""
        assert dbu.should_skip_file('@eaDir') is True
        assert dbu.should_skip_file('@recycle') is True

    def test_skip_pyc_files(self):
        """Test that .pyc and .pyo files are skipped."""
        assert dbu.should_skip_file('module.pyc') is True
        assert dbu.should_skip_file('script.pyo') is True
        assert dbu.should_skip_file('cache.pyc') is True

    def test_normal_files_not_skipped(self):
        """Test that normal files are not skipped."""
        assert dbu.should_skip_file('photo.jpg') is False
        assert dbu.should_skip_file('video.h264') is False
        assert dbu.should_skip_file('document.txt') is False
        assert dbu.should_skip_file('image.png') is False

    def test_byte_string_input(self):
        """Test handling of byte string input."""
        assert dbu.should_skip_file(b'.hidden_file') is True
        assert dbu.should_skip_file(b'normal_file.txt') is False
        assert dbu.should_skip_file(b'test.pyc') is True

    def test_non_text_input(self):
        """Test handling of non-text input."""
        class NonString:
            def __str__(self):
                return '.hidden'
        
        # Should handle gracefully by converting to string
        result = dbu.should_skip_file(NonString())
        assert result is True


class TestShouldSkipDirectory:
    """Tests for should_skip_directory function."""

    def test_skip_hidden_directories(self):
        """Test that hidden directories (starting with .) are skipped."""
        assert dbu.should_skip_directory('.git') is True
        assert dbu.should_skip_directory('.cache') is True
        assert dbu.should_skip_directory('.config') is True

    def test_skip_pycache(self):
        """Test that __pycache__ directories are skipped."""
        assert dbu.should_skip_directory('__pycache__') is True

    def test_skip_temp_directories_tilde(self):
        """Test that directories ending with ~ are skipped."""
        assert dbu.should_skip_directory('backup~') is True
        assert dbu.should_skip_directory('~temp') is True

    def test_skip_temp_directories_at(self):
        """Test that directories starting with @ are skipped."""
        assert dbu.should_skip_directory('@eaDir') is True
        assert dbu.should_skip_directory('@recycle') is True

    def test_normal_directories_not_skipped(self):
        """Test that normal directories are not skipped."""
        assert dbu.should_skip_directory('photos') is False
        assert dbu.should_skip_directory('videos') is False
        assert dbu.should_skip_directory('documents') is False
        assert dbu.should_skip_directory('2024') is False


class TestListFolder:
    """Tests for list_folder function."""

    def test_list_folder_success(self):
        """Test successful folder listing."""
        dbx = MagicMock()
        
        # Create mock entries
        entry1 = MagicMock()
        entry1.name = 'file1.jpg'
        entry2 = MagicMock()
        entry2.name = 'file2.jpg'
        
        dbx.files_list_folder.return_value = MagicMock(entries=[entry1, entry2])
        
        result = dbu.list_folder(dbx, 'Downloads', '')
        
        assert 'file1.jpg' in result
        assert 'file2.jpg' in result
        assert len(result) == 2
        dbx.files_list_folder.assert_called_once_with('/Downloads')

    def test_list_folder_with_subfolder(self):
        """Test listing folder with subfolder path."""
        dbx = MagicMock()
        
        entry = MagicMock()
        entry.name = 'photo.jpg'
        dbx.files_list_folder.return_value = MagicMock(entries=[entry])
        
        result = dbu.list_folder(dbx, 'Downloads', '2024/01')
        
        dbx.files_list_folder.assert_called_once_with('/Downloads/2024/01')
        assert 'photo.jpg' in result

    def test_list_folder_api_error(self):
        """Test handling of API error returns empty dict."""
        dbx = MagicMock()
        
        dbx.files_list_folder.side_effect = ApiError(
            error='path_error',
            user_message_text='Path error',
            user_message_locale='en'
        )
        
        result = dbu.list_folder(dbx, 'Downloads', '')
        
        assert result == {}

    def test_list_folder_double_slash_cleanup(self):
        """Test that double slashes in path are cleaned up."""
        dbx = MagicMock()
        
        entry = MagicMock()
        entry.name = 'test.jpg'
        dbx.files_list_folder.return_value = MagicMock(entries=[entry])
        
        result = dbu.list_folder(dbx, 'Downloads', 'folder//subfolder')
        
        dbx.files_list_folder.assert_called_once_with('/Downloads/folder/subfolder')


class TestDownload:
    """Tests for download function."""

    def test_download_success(self):
        """Test successful file download."""
        dbx = MagicMock()
        
        mock_md = MagicMock()
        mock_response = MagicMock()
        mock_response.content = b'file content here'
        
        dbx.files_download.return_value = (mock_md, mock_response)
        
        result = dbu.download(dbx, 'Downloads', '', 'test.jpg')
        
        assert result == b'file content here'
        dbx.files_download.assert_called_once_with('/Downloads/test.jpg')

    def test_download_http_error(self):
        """Test handling of HTTP error returns None."""
        dbx = MagicMock()
        
        dbx.files_download.side_effect = HttpError("File not found")
        
        result = dbu.download(dbx, 'Downloads', '', 'test.jpg')
        
        assert result is None

    def test_download_with_subfolder(self):
        """Test download with subfolder path."""
        dbx = MagicMock()
        
        mock_md = MagicMock()
        mock_response = MagicMock()
        mock_response.content = b'test data'
        
        dbx.files_download.return_value = (mock_md, mock_response)
        
        result = dbu.download(dbx, 'Downloads', '2024/01', 'photo.jpg')
        
        assert result == b'test data'
        dbx.files_download.assert_called_once_with('/Downloads/2024/01/photo.jpg')


class TestUpload:
    """Tests for upload function."""

    def test_upload_success(self):
        """Test successful file upload."""
        dbx = MagicMock()
        
        # Create a temp file for testing
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.jpg') as f:
            f.write(b'test image data')
            temp_path = f.name
        
        try:
            mock_response = MagicMock()
            mock_response.name = b'test.jpg'
            dbx.files_upload.return_value = mock_response
            
            result = dbu.upload(dbx, temp_path, 'Downloads', '', 'test.jpg')
            
            assert result is not None
            assert result.name == b'test.jpg'
            dbx.files_upload.assert_called()
        finally:
            os.unlink(temp_path)

    def test_upload_with_overwrite(self):
        """Test upload with overwrite mode."""
        dbx = MagicMock()
        
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.jpg') as f:
            f.write(b'overwrite test')
            temp_path = f.name
        
        try:
            mock_response = MagicMock()
            mock_response.name = b'existing.jpg'
            dbx.files_upload.return_value = mock_response
            
            result = dbu.upload(dbx, temp_path, 'Downloads', '', 
                              'existing.jpg', overwrite=True)
            
            assert result is not None
            # Verify overwrite mode was used
            call_args = dbx.files_upload.call_args
            assert call_args[0][2] == _sys_dropbox.files.WriteMode.overwrite
        finally:
            os.unlink(temp_path)

    def test_upload_api_error(self):
        """Test handling of API error returns None."""
        dbx = MagicMock()
        
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.jpg') as f:
            f.write(b'test data')
            temp_path = f.name
        
        try:
            dbx.files_upload.side_effect = ApiError(
                error='upload_failed',
                user_message_text='Upload failed',
                user_message_locale='en'
            )
            
            result = dbu.upload(dbx, temp_path, 'Downloads', '', 'test.jpg')
            
            assert result is None
        finally:
            os.unlink(temp_path)

    def test_upload_with_subfolder(self):
        """Test upload with subfolder path."""
        dbx = MagicMock()
        
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.jpg') as f:
            f.write(b'subfolder test')
            temp_path = f.name
        
        try:
            mock_response = MagicMock()
            mock_response.name = b'2024/01/photo.jpg'
            dbx.files_upload.return_value = mock_response
            
            result = dbu.upload(dbx, temp_path, 'Downloads', 
                              '2024/01', 'photo.jpg')
            
            assert result is not None
            dbx.files_upload.assert_called()
        finally:
            os.unlink(temp_path)


class TestYesNo:
    """Tests for yesno function."""

    def test_yesno_default_true_with_blank(self):
        """Test that blank input returns default True."""
        args = MagicMock(yes=False, no=False, default=False)
        
        with patch('dropbox_upload.input', return_value=''):
            result = dbu.yesno('Test message', True, args)
        
        assert result is True

    def test_yesno_default_false_with_blank(self):
        """Test that blank input returns default False."""
        args = MagicMock(yes=False, no=False, default=False)
        
        with patch('dropbox_upload.input', return_value=''):
            result = dbu.yesno('Test message', False, args)
        
        assert result is False

    def test_yesno_yes_answer(self):
        """Test that yes/answer returns True."""
        args = MagicMock(yes=False, no=False, default=False)
        
        with patch('dropbox_upload.input', return_value='yes'):
            result = dbu.yesno('Test message', False, args)
        
        assert result is True

    def test_yesno_y_answer(self):
        """Test that y/answer returns True."""
        args = MagicMock(yes=False, no=False, default=False)
        
        with patch('dropbox_upload.input', return_value='y'):
            result = dbu.yesno('Test message', False, args)
        
        assert result is True

    def test_yesno_no_answer(self):
        """Test that no/answer returns False."""
        args = MagicMock(yes=False, no=False, default=False)
        
        with patch('dropbox_upload.input', return_value='no'):
            result = dbu.yesno('Test message', True, args)
        
        assert result is False

    def test_yesno_n_answer(self):
        """Test that n/answer returns False."""
        args = MagicMock(yes=False, no=False, default=False)
        
        with patch('dropbox_upload.input', return_value='n'):
            result = dbu.yesno('Test message', True, args)
        
        assert result is False

    def test_yesno_case_insensitive(self):
        """Test that answers are case-insensitive."""
        args = MagicMock(yes=False, no=False, default=False)
        
        with patch('dropbox_upload.input', return_value='YES'):
            result = dbu.yesno('Test', False, args)
        
        assert result is True
        
        with patch('dropbox_upload.input', return_value='No'):
            result = dbu.yesno('Test', True, args)
        
        assert result is False

    def test_yesno_force_yes(self):
        """Test that --yes flag forces yes."""
        args = MagicMock(yes=True, no=False, default=False)
        
        # input should not be called when --yes is set
        with patch('dropbox_upload.input') as mock_input:
            result = dbu.yesno('Test message', False, args)
        
        assert result is True
        mock_input.assert_not_called()

    def test_yesno_force_no(self):
        """Test that --no flag forces no."""
        args = MagicMock(yes=False, no=True, default=False)
        
        with patch('dropbox_upload.input') as mock_input:
            result = dbu.yesno('Test message', True, args)
        
        assert result is False
        mock_input.assert_not_called()

    def test_yesno_force_default(self):
        """Test that --default flag uses default answer."""
        args = MagicMock(yes=False, no=False, default=True)
        
        with patch('dropbox_upload.input') as mock_input:
            result = dbu.yesno('Test message', False, args)
        
        assert result is False  # Default answer was False
        mock_input.assert_not_called()

    def test_yesno_quit_command(self):
        """Test that quit/q command raises SystemExit."""
        args = MagicMock(yes=False, no=False, default=False)
        
        with pytest.raises(SystemExit):
            with patch('dropbox_upload.input', return_value='quit'):
                dbu.yesno('Test message', False, args)

    def test_yesno_pdb_command(self):
        """Test that pdb/p command imports pdb (doesn't fail)."""
        args = MagicMock(yes=False, no=False, default=False)
        
        # pdb.set_trace() would hang, so we just verify it's importable
        with patch('dropbox_upload.input', return_value='pdb'):
            mock_pdb_module = MagicMock()
            mock_pdb_module.set_trace.side_effect = SystemExit("pdb exit")
            
            with patch.dict('sys.modules', {'pdb': mock_pdb_module}):
                try:
                    dbu.yesno('Test message', False, args)
                except SystemExit as e:
                    # Verify pdb was imported and set_trace was called
                    assert str(e) == "pdb exit"
                    mock_pdb_module.set_trace.assert_called_once()

    def test_yesno_invalid_answer_retry(self):
        """Test that invalid answers prompt retry."""
        args = MagicMock(yes=False, no=False, default=False)
        
        # First call returns invalid, second returns valid
        call_count = [0]
        def mock_input_side_effect(prompt):
            call_count[0] += 1
            if call_count[0] == 1:
                return 'invalid'
            return 'yes'
        
        with patch('dropbox_upload.input', side_effect=mock_input_side_effect):
            result = dbu.yesno('Test message', False, args)
        
        assert result is True
        assert call_count[0] == 2


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_should_skip_edge_cases(self):
        """Test edge cases in file skipping logic."""
        # Unicode handling
        assert dbu.should_skip_file('文件.jpg') is False
        assert dbu.should_skip_file('файл.jpg') is False
        
        # Mixed case extensions
        assert dbu.should_skip_file('file.PYC') is False  # Case sensitive
        assert dbu.should_skip_file('file.pyc') is True
        
        # Files with multiple dots
        assert dbu.should_skip_file('.hidden.txt') is True
        assert dbu.should_skip_file('file.backup~') is True
        
        # Empty and None-like strings
        assert dbu.should_skip_file('') is False
        assert dbu.should_skip_file('.') is True

    def test_directory_skipping_patterns(self):
        """Test directory skipping patterns."""
        # Standard directories
        assert dbu.should_skip_directory('My Documents') is False
        assert dbu.should_skip_directory('Photos 2024') is False

        # System directories
        assert dbu.should_skip_directory('System Volume Information') is False
        assert dbu.should_skip_directory('.Trash-1000') is True

        # Special characters
        assert dbu.should_skip_directory('@Recycle') is True
        assert dbu.should_skip_directory('~backup') is True

    def test_should_skip_file_integration_with_main_logic(self):
        """Test that should_skip_file matches main() file skipping logic."""
        # Files that should be skipped (matching main() logic)
        skipped_files = ['.gitignore', '.bashrc', 'file.txt~', 
                        '@eaDir', '~temp', 'test.pyc', 'cache.pyo']
        for f in skipped_files:
            assert dbu.should_skip_file(f) is True, f"File {f} should be skipped"

        # Files that should NOT be skipped
        normal_files = ['photo.jpg', 'video.h264', 'document.txt', 
                       'image.png', 'MyFile.jpg', 'test_2024.jpg']
        for f in normal_files:
            assert dbu.should_skip_file(f) is False, f"File {f} should not be skipped"

    def test_should_skip_directory_integration_with_main_logic(self):
        """Test that should_skip_directory matches main() directory skipping logic."""
        # Directories that should be skipped (matching main() logic)
        skipped_dirs = ['.git', '.cache', '.config', 'backup~', 
                       '~temp', '@eaDir', '__pycache__']
        for d in skipped_dirs:
            assert dbu.should_skip_directory(d) is True, f"Directory {d} should be skipped"

        # Directories that should NOT be skipped
        normal_dirs = ['photos', 'videos', 'documents', '2024',
                      'My Documents', 'Photos 2024']
        for d in normal_dirs:
            assert dbu.should_skip_directory(d) is False, f"Directory {d} should not be skipped"
