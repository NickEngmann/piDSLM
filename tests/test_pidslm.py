"""Tests for pidslm.py - Raspberry Pi DSLR Camera Controller"""

import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the repo directory to the path
sys.path.insert(0, '')


def test_app_initialization(source_module):
    """Test that the piDSLM app initializes correctly"""
    with patch('pidslm.App') as mock_app, \
         patch('pidslm.PushButton') as mock_button, \
         patch('pidslm.Text') as mock_text, \
         patch('pidslm.Picture') as mock_picture, \
         patch('pidslm.Window') as mock_window:
        
        mock_app_instance = MagicMock()
        mock_app.return_value = mock_app_instance
        
        # Initialize the app
        app = source_module.piDSLM()
        
        # Verify app was created
        assert app is not None
        mock_app.assert_called_once()


def test_capture_photo(source_module):
    """Test photo capture functionality"""
    with patch('pidslm.App') as mock_app, \
         patch('pidslm.PushButton') as mock_button, \
         patch('pidslm.Text') as mock_text, \
         patch('pidslm.Picture') as mock_picture, \
         patch('pidslm.Window') as mock_window, \
         patch('pidslm.subprocess') as mock_subprocess, \
         patch('pidslm.time') as mock_time, \
         patch('pidslm.datetime') as mock_datetime:
        
        mock_app_instance = MagicMock()
        mock_app.return_value = mock_app_instance
        
        app = source_module.piDSLM()
        
        # Mock the subprocess call for photo capture
        mock_subprocess.run.return_value = MagicMock(returncode=0)
        mock_datetime.datetime.now.return_value.strftime.return_value = '20240101_120000'
        
        # Test photo capture
        result = app.capture_photo()
        
        # Verify subprocess was called with correct parameters
        assert mock_subprocess.run.called
        assert 'raspistill' in str(mock_subprocess.run.call_args)


def test_start_video(source_module):
    """Test video recording start functionality"""
    with patch('pidslm.App') as mock_app, \
         patch('pidslm.PushButton') as mock_button, \
         patch('pidslm.Text') as mock_text, \
         patch('pidslm.Picture') as mock_picture, \
         patch('pidslm.Window') as mock_window, \
         patch('pidslm.subprocess') as mock_subprocess, \
         patch('pidslm.time') as mock_time, \
         patch('pidslm.datetime') as mock_datetime:
        
        mock_app_instance = MagicMock()
        mock_app.return_value = mock_app_instance
        
        app = source_module.piDSLM()
        
        # Mock the subprocess call for video recording
        mock_subprocess.Popen.return_value = MagicMock(pid=1234)
        mock_datetime.datetime.now.return_value.strftime.return_value = '20240101_120000'
        
        # Test video start
        result = app.start_video()
        
        # Verify subprocess.Popen was called
        assert mock_subprocess.Popen.called
        assert 'raspivid' in str(mock_subprocess.Popen.call_args)


def test_stop_video(source_module):
    """Test video recording stop functionality"""
    with patch('pidslm.App') as mock_app, \
         patch('pidslm.PushButton') as mock_button, \
         patch('pidslm.Text') as mock_text, \
         patch('pidslm.Picture') as mock_picture, \
         patch('pidslm.Window') as mock_window, \
         patch('pidslm.subprocess') as mock_subprocess, \
         patch('pidslm.time') as mock_time:
        
        mock_app_instance = MagicMock()
        mock_app.return_value = mock_app_instance
        
        app = source_module.piDSLM()
        
        # Mock a running video process
        mock_process = MagicMock()
        mock_process.pid = 1234
        app.video_process = mock_process
        
        # Test video stop
        result = app.stop_video()
        
        # Verify the process was terminated
        if app.video_process:
            assert app.video_process.terminate.called or app.video_process.kill.called


def test_upload_to_dropbox(source_module):
    """Test Dropbox upload functionality"""
    with patch('pidslm.App') as mock_app, \
         patch('pidslm.PushButton') as mock_button, \
         patch('pidslm.Text') as mock_text, \
         patch('pidslm.Picture') as mock_picture, \
         patch('pidslm.Window') as mock_window, \
         patch('pidslm.subprocess') as mock_subprocess:
        
        mock_app_instance = MagicMock()
        mock_app.return_value = mock_app_instance
        
        app = source_module.piDSLM()
        
        # Mock the subprocess call for upload
        mock_subprocess.Popen.return_value = MagicMock(pid=1234)
        
        # Test upload
        app.upload_to_dropbox()
        
        # Verify subprocess was called with correct parameters
        assert mock_subprocess.Popen.called
        call_args = str(mock_subprocess.Popen.call_args)
        assert 'dropbox_upload.py' in call_args
        assert '--yes' in call_args


def test_hide_busy(source_module):
    """Test the hide_busy method"""
    with patch('pidslm.App') as mock_app, \
         patch('pidslm.PushButton') as mock_button, \
         patch('pidslm.Text') as mock_text, \
         patch('pidslm.Picture') as mock_picture, \
         patch('pidslm.Window') as mock_window:
        
        mock_app_instance = MagicMock()
        mock_app.return_value = mock_app_instance
        
        app = source_module.piDSLM()
        
        # Test hide_busy
        app.hide_busy()
        
        # Verify the busy text was hidden
        assert mock_app_instance.hide.called


def test_show_busy(source_module):
    """Test the show_busy method"""
    with patch('pidslm.App') as mock_app, \
         patch('pidslm.PushButton') as mock_button, \
         patch('pidslm.Text') as mock_text, \
         patch('pidslm.Picture') as mock_picture, \
         patch('pidslm.Window') as mock_window:
        
        mock_app_instance = MagicMock()
        mock_app.return_value = mock_app_instance
        
        app = source_module.piDSLM()
        
        # Test show_busy
        app.show_busy()
        
        # Verify the busy text was shown
        assert mock_app_instance.show.called


def test_cleanup(source_module):
    """Test the cleanup method for GPIO cleanup"""
    with patch('pidslm.App') as mock_app, \
         patch('pidslm.PushButton') as mock_button, \
         patch('pidslm.Text') as mock_text, \
         patch('pidslm.Picture') as mock_picture, \
         patch('pidslm.Window') as mock_window, \
         patch('pidslm.GPIO') as mock_gpio:
        
        mock_app_instance = MagicMock()
        mock_app.return_value = mock_app_instance
        
        app = source_module.piDSLM()
        
        # Test cleanup
        app.cleanup()
        
        # Verify GPIO cleanup was called
        assert mock_gpio.cleanup.called


def test_run_method(source_module):
    """Test the run method starts the app"""
    with patch('pidslm.App') as mock_app, \
         patch('pidslm.PushButton') as mock_button, \
         patch('pidslm.Text') as mock_text, \
         patch('pidslm.Picture') as mock_picture, \
         patch('pidslm.Window') as mock_window:
        
        mock_app_instance = MagicMock()
        mock_app.return_value = mock_app_instance
        
        app = source_module.piDSLM()
        
        # Test run
        app.run()
        
        # Verify app.display was called
        assert mock_app_instance.display.called
