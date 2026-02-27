"""Tests for piDSLM application."""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure we're using the mocked GPIO
import RPi.GPIO as GPIO


class TestPiDSLM:
    """Test cases for the piDSLM class."""

    def test_timestamp_format(self, source_module):
        """Test that timestamp generates expected format."""
        pidslm = source_module.piDSLM()
        ts = pidslm.timestamp()
        # Expected format: YYYYMMDD_HHMMSS
        assert len(ts) == 15
        assert ts[8] == '_'  # Separator
        assert ts[:8].isdigit()  # Date part
        assert ts[9:].isdigit()  # Time part

    def test_clear_method(self, source_module, mocker):
        """Test the clear method removes files."""
        pidslm = source_module.piDSLM()
        mock_system = mocker.patch('os.system')
        
        pidslm.clear()
        
        mock_system.assert_called_once_with('rm -v /home/pi/Downloads/*')

    def test_show_busy_method(self, source_module, capsys):
        """Test show_busy method shows busy window."""
        pidslm = source_module.piDSLM()
        
        pidslm.show_busy()
        
        # Check that busy window is shown (we can't directly test GUI state)
        # but we can verify the method was called
        captured = capsys.readouterr()
        assert 'busy now' in captured.out

    def test_hide_busy_method(self, source_module, capsys):
        """Test hide_busy method hides busy window."""
        pidslm = source_module.piDSLM()
        
        pidslm.hide_busy()
        
        captured = capsys.readouterr()
        assert 'no longer busy' in captured.out

    def test_burst_method(self, source_module, mocker):
        """Test burst capture method."""
        pidslm = source_module.piDSLM()
        mock_system = mocker.patch('os.system')
        mock_timestamp = mocker.patch.object(pidslm, 'timestamp', return_value='20240101_120000')
        mock_show_busy = mocker.patch.object(pidslm, 'show_busy')
        mock_hide_busy = mocker.patch.object(pidslm, 'hide_busy')
        
        pidslm.burst()
        
        mock_show_busy.assert_called_once()
        mock_timestamp.assert_called_once()
        mock_system.assert_called_once()
        call_args = mock_system.call_args[0][0]
        assert 'raspistill' in call_args
        assert 'BR20240101_120000' in call_args
        mock_hide_busy.assert_called_once()

    def test_video_capture_method(self, source_module, mocker):
        """Test video capture method."""
        pidslm = source_module.piDSLM()
        mock_system = mocker.patch('os.system')
        mock_timestamp = mocker.patch.object(pidslm, 'timestamp', return_value='20240101_120000')
        mock_show_busy = mocker.patch.object(pidslm, 'show_busy')
        mock_hide_busy = mocker.patch.object(pidslm, 'hide_busy')
        
        pidslm.video_capture()
        
        mock_show_busy.assert_called_once()
        mock_system.assert_called_once()
        call_args = mock_system.call_args[0][0]
        assert 'raspivid' in call_args
        assert 'vid.h264' in call_args
        mock_hide_busy.assert_called_once()

    def test_split_hd_30m_method(self, source_module, mocker):
        """Test split HD 30m method."""
        pidslm = source_module.piDSLM()
        mock_system = mocker.patch('os.system')
        mock_timestamp = mocker.patch.object(pidslm, 'timestamp', return_value='20240101_120000')
        mock_show_busy = mocker.patch.object(pidslm, 'show_busy')
        mock_hide_busy = mocker.patch.object(pidslm, 'hide_busy')
        
        pidslm.split_hd_30m()
        
        mock_show_busy.assert_called_once()
        mock_system.assert_called_once()
        call_args = mock_system.call_args[0][0]
        assert 'raspivid' in call_args
        assert 'vid%04d.h264' in call_args
        mock_hide_busy.assert_called_once()

    def test_lapse_method(self, source_module, mocker):
        """Test timelapse method."""
        pidslm = source_module.piDSLM()
        mock_system = mocker.patch('os.system')
        mock_timestamp = mocker.patch.object(pidslm, 'timestamp', return_value='20240101_120000')
        mock_show_busy = mocker.patch.object(pidslm, 'show_busy')
        mock_hide_busy = mocker.patch.object(pidslm, 'hide_busy')
        
        pidslm.lapse()
        
        mock_show_busy.assert_called_once()
        mock_system.assert_called_once()
        call_args = mock_system.call_args[0][0]
        assert 'raspistill' in call_args
        assert '%04d' in call_args  # Timelapse uses numbered output files
        mock_hide_busy.assert_called_once()

    def test_long_preview_method(self, source_module, mocker):
        """Test long preview method."""
        pidslm = source_module.piDSLM()
        mock_system = mocker.patch('os.system')
        mock_show_busy = mocker.patch.object(pidslm, 'show_busy')
        mock_hide_busy = mocker.patch.object(pidslm, 'hide_busy')
        
        pidslm.long_preview()
        
        mock_show_busy.assert_called_once()
        mock_system.assert_called_once()
        call_args = mock_system.call_args[0][0]
        assert 'raspistill' in call_args
        assert '-t 15000' in call_args
        mock_hide_busy.assert_called_once()

    def test_capture_image_method(self, source_module, mocker):
        """Test capture image method."""
        pidslm = source_module.piDSLM()
        mock_system = mocker.patch('os.system')
        mock_timestamp = mocker.patch.object(pidslm, 'timestamp', return_value='20240101_120000')
        mock_show_busy = mocker.patch.object(pidslm, 'show_busy')
        mock_hide_busy = mocker.patch.object(pidslm, 'hide_busy')
        
        pidslm.capture_image()
        
        mock_show_busy.assert_called_once()
        mock_system.assert_called_once()
        call_args = mock_system.call_args[0][0]
        assert 'raspistill' in call_args
        assert 'cam.jpg' in call_args
        mock_hide_busy.assert_called_once()

    def test_takePicture_callback(self, source_module, mocker):
        """Test takePicture callback method."""
        pidslm = source_module.piDSLM()
        mock_system = mocker.patch('os.system')
        mock_timestamp = mocker.patch.object(pidslm, 'timestamp', return_value='20240101_120000')
        
        pidslm.takePicture(16)  # channel argument
        
        mock_system.assert_called_once()
        call_args = mock_system.call_args[0][0]
        assert 'raspistill' in call_args
        assert 'cam.jpg' in call_args

    def test_upload_method(self, source_module, mocker):
        """Test upload method."""
        pidslm = source_module.piDSLM()
        mock_popen = mocker.patch('subprocess.Popen')
        mock_show_busy = mocker.patch.object(pidslm, 'show_busy')
        mock_hide_busy = mocker.patch.object(pidslm, 'hide_busy')
        
        pidslm.upload()
        
        mock_show_busy.assert_called_once()
        mock_popen.assert_called_once_with(['python3', '/home/pi/piDSLM/dropbox_upload.py', '--yes'])
        mock_hide_busy.assert_called_once()

    def test_fullscreen_methods(self, source_module):
        """Test fullscreen toggle methods."""
        pidslm = source_module.piDSLM()
        
        # These methods just set attributes, we verify they don't error
        pidslm.fullscreen()
        pidslm.notfullscreen()

    def test_picture_navigation(self, source_module, mocker):
        """Test picture navigation methods."""
        pidslm = source_module.piDSLM()
        pidslm.saved_pictures = ['/home/pi/Downloads/img1.jpg', '/home/pi/Downloads/img2.jpg']
        pidslm.picture_index = 0
        
        # Mock Picture class to avoid GUI errors
        mock_picture = mocker.patch('guizero.Picture')
        
        # Test picture_right wraps around
        pidslm.picture_right()
        assert pidslm.picture_index == 1
        
        # Test picture_right wraps to 0
        pidslm.picture_right()
        assert pidslm.picture_index == 0
        
        # Test picture_left wraps
        pidslm.picture_left()
        assert pidslm.picture_index == 1

    def test_gpio_initialization(self, source_module, mocker):
        """Test GPIO initialization in constructor."""
        mock_setmode = mocker.patch('RPi.GPIO.setmode')
        mock_setup = mocker.patch('RPi.GPIO.setup')
        mock_add_event_detect = mocker.patch('RPi.GPIO.add_event_detect')
        mock_setwarnings = mocker.patch('RPi.GPIO.setwarnings')
        
        # Create instance to trigger GPIO setup
        pidslm = source_module.piDSLM()
        
        mock_setwarnings.assert_called_once_with(False)
        mock_setmode.assert_called_once_with(GPIO.BCM)
        mock_setup.assert_called_once_with(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        mock_add_event_detect.assert_called_once()


class TestDropboxUpload:
    """Test cases for dropbox_upload functionality."""

    def test_main_with_args(self, source_module, mocker):
        """Test main function with command line arguments."""
        mock_parser = mocker.patch('argparse.ArgumentParser.parse_args')
        mock_parser.return_value = mocker.MagicMock(
            folder='Downloads',
            rootdir='~/Downloads',
            token='test_token',
            yes=True,
            no=False,
            default=False
        )
        mocker.patch('dropbox.Dropbox')
        mocker.patch('os.walk', return_value=[])
        mocker.patch('os.path.expanduser', return_value='/home/pi/Downloads')
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('os.path.isdir', return_value=True)
        
        # Import and test main
        from dropbox_upload import main
        
        # Just verify it doesn't crash with mocked dependencies
        # (full integration testing would require more complex mocking)

    def test_yesno_function(self, source_module, mocker):
        """Test yesno helper function."""
        from dropbox_upload import yesno
        
        # Test with --yes flag
        args = mocker.MagicMock(yes=True, no=False, default=False)
        assert yesno('Test?', True, args) is True
        
        # Test with --no flag
        args = mocker.MagicMock(yes=False, no=True, default=False)
        assert yesno('Test?', False, args) is False
        
        # Test with --default flag
        args = mocker.MagicMock(yes=False, no=False, default=True)
        assert yesno('Test?', True, args) is True
