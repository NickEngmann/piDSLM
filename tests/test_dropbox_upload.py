"""Tests for dropbox_upload.py - Dropbox upload functionality.

Tests the file scanning, upload logic, and argument parsing.
"""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch, call

# Import module functions
import dropbox_upload


def test_parse_args():
    """Test argument parsing with default values."""
    with patch('dropbox_upload.os') as mock_os:
        mock_os.environ.get.return_value = 'test_token'
        
        with patch('dropbox_upload.argparse') as mock_argparse:
            mock_parser = MagicMock()
            mock_argparse.ArgumentParser.return_value = mock_parser
            mock_parser.parse_args.return_value = MagicMock(
                folder='Downloads',
                rootdir='/tmp/downloads',
                token='test_token',
                yes=False,
                no=False,
                default=False,
                count=0
            )
            
            args = dropbox_upload.parse_args()
            
            assert args.token == 'test_token'


def test_parse_args_with_count():
    """Test argument parsing with --count flag."""
    with patch('dropbox_upload.os') as mock_os:
        mock_os.environ.get.return_value = 'test_token'
        
        with patch('dropbox_upload.sys') as mock_sys:
            mock_sys.argv = ['dropbox_upload.py', '--yes', '--count', '5']
            
            with patch('dropbox_upload.argparse') as mock_argparse:
                mock_parser = MagicMock()
                mock_argparse.ArgumentParser.return_value = mock_parser
                mock_parser.parse_args.return_value = MagicMock(
                    folder='Downloads',
                    rootdir='/tmp/downloads',
                    token='test_token',
                    yes=True,
                    no=False,
                    default=False,
                    count=5
                )
                
                args = dropbox_upload.parse_args()
                
                assert args.yes is True
                assert args.count == 5


def test_should_skip_file():
    """Test file skipping logic."""
    skip, reason = dropbox_upload.should_skip_file('.hidden')
    assert skip is True
    assert reason == 'dot file'
    
    skip, reason = dropbox_upload.should_skip_file('temp~')
    assert skip is True
    assert reason == 'temporary file'
    
    skip, reason = dropbox_upload.should_skip_file('test.pyc')
    assert skip is True
    assert reason == 'generated file'
    
    skip, reason = dropbox_upload.should_skip_file('normal.jpg')
    assert skip is False
    assert reason is None


def test_should_skip_directory():
    """Test directory skipping logic."""
    skip, reason = dropbox_upload.should_skip_directory('.git')
    assert skip is True
    assert reason == 'dot directory'
    
    skip, reason = dropbox_upload.should_skip_directory('__pycache__')
    assert skip is True
    assert reason == 'generated directory'
    
    skip, reason = dropbox_upload.should_skip_directory('photos')
    assert skip is False
    assert reason is None


def test_files_to_upload():
    """Test file scanning logic."""
    with patch('dropbox_upload.os') as mock_os:
        mock_os.walk.return_value = [
            ('/tmp/downloads', [], ['photo1.jpg', 'photo2.jpg']),
        ]
        mock_os.path.sep = '/'
        
        files = dropbox_upload.files_to_upload('/tmp/downloads', 'Downloads', max_files=0)
        
        assert len(files) == 2
        assert files[0][1] == 'photo1.jpg'
        assert files[1][1] == 'photo2.jpg'


def test_files_to_upload_with_limit():
    """Test file scanning with max_files limit."""
    with patch('dropbox_upload.os') as mock_os:
        mock_os.walk.return_value = [
            ('/tmp/downloads', [], ['photo1.jpg', 'photo2.jpg', 'photo3.jpg']),
        ]
        mock_os.path.sep = '/'
        
        files = dropbox_upload.files_to_upload('/tmp/downloads', 'Downloads', max_files=2)
        
        assert len(files) == 2


def test_files_to_upload_with_skips():
    """Test file scanning skips hidden/temporary files."""
    with patch('dropbox_upload.os') as mock_os:
        mock_os.walk.return_value = [
            ('/tmp/downloads', [], ['.hidden', 'temp~', 'normal.jpg']),
        ]
        mock_os.path.sep = '/'
        
        files = dropbox_upload.files_to_upload('/tmp/downloads', 'Downloads', max_files=0)
        
        assert len(files) == 1
        assert files[0][1] == 'normal.jpg'


def test_list_folder():
    """Test Dropbox folder listing."""
    mock_dbx = MagicMock()
    mock_listing = MagicMock()
    mock_entry = MagicMock()
    mock_entry.name = 'photo1.jpg'
    mock_listing.entries = [mock_entry]
    mock_dbx.files_list_folder.return_value = mock_listing
    
    result = dropbox_upload.list_folder(mock_dbx, 'Downloads', '')
    
    assert 'photo1.jpg' in result


def test_upload_file():
    """Test file upload logic."""
    mock_dbx = MagicMock()
    mock_response = MagicMock()
    mock_response.name = 'uploaded_photo.jpg'
    mock_dbx.files_upload.return_value = mock_response
    
    with patch('builtins.open') as mock_open:
        mock_file = MagicMock()
        mock_file.read.return_value = b'binary_data'
        mock_open.return_value.__enter__.return_value = mock_file
        
        with patch('dropbox_upload.os.path.getmtime', return_value=1234567890.0):
            result = dropbox_upload.upload_file(
                mock_dbx, '/tmp/photo.jpg', 'Downloads', '', 'photo.jpg'
            )
            
            assert result == mock_response


def test_upload_files():
    """Test bulk upload operation."""
    mock_dbx = MagicMock()
    
    with patch('dropbox_upload.files_to_upload') as mock_scan:
        mock_scan.return_value = [
            ('/tmp/photo1.jpg', 'photo1.jpg', 'Downloads'),
            ('/tmp/photo2.jpg', 'photo2.jpg', 'Downloads'),
        ]
        
        with patch('dropbox_upload.list_folder') as mock_list:
            mock_list.return_value = {}
            
            with patch('dropbox_upload.upload_file') as mock_upload:
                mock_upload.return_value = MagicMock(name='uploaded')
                
                result = dropbox_upload.upload_files(mock_dbx, '/tmp', 'Downloads', max_files=0)
                
                assert result['total'] == 2
                assert result['success'] == 2


def test_stopwatch():
    """Test stopwatch context manager."""
    with dropbox_upload.stopwatch('test_operation'):
        pass  # Context manager test


def test_yesno_default():
    """Test yesno with default argument."""
    mock_args = MagicMock(yes=False, no=False, default=True)
    
    result = dropbox_upload.yesno('Test message', True, mock_args)
    assert result is True


def test_yesno_yes_flag():
    """Test yesno with --yes flag."""
    mock_args = MagicMock(yes=True, no=False, default=False)
    
    result = dropbox_upload.yesno('Test message', False, mock_args)
    assert result is True


def test_yesno_no_flag():
    """Test yesno with --no flag."""
    mock_args = MagicMock(yes=False, no=True, default=False)
    
    result = dropbox_upload.yesno('Test message', True, mock_args)
    assert result is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
