"""Tests for piDSLM - Raspberry Pi DSLR Camera Controller"""

import pytest
import os
import sys
import glob
from unittest.mock import patch, MagicMock


def test_app_initialization(source_module):
    """Test that the piDSLM app initializes correctly"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            # Mock the app display method
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            
            # Mock Window
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            # Initialize the app
            app = source_module.piDSLM()
            
            # Verify app was created
            assert app.app is not None
            assert app.busy is not None
            assert app.capture_number is not None
            assert app.video_capture_number is not None


def test_timestamp_generation(source_module):
    """Test that timestamp generation works correctly"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            timestamp = app.timestamp()
            
            # Verify timestamp format (YYYYMMDD_HHMMSS) - 15 characters
            assert len(timestamp) == 15
            assert timestamp[8] == '_'  # Separator
            # Verify it's a valid date/time format
            assert timestamp[:8].isdigit()  # Date part
            assert timestamp[9:].isdigit()  # Time part


def test_clear_folder(source_module):
    """Test the clear folder functionality"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            # Mock os.system to capture the command
            with patch('os.system') as mock_system:
                app.clear()
                # Verify the rm command was called
                mock_system.assert_called_once()
                assert 'rm -v /home/pi/Downloads/*' in mock_system.call_args[0][0]


def test_show_hide_busy(source_module):
    """Test show and hide busy window functionality"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            
            # Track show/hide calls
            busy_shown = []
            busy_hidden = []
            
            def track_show():
                busy_shown.append(True)
            def track_hide():
                busy_hidden.append(True)
            
            mock_window.return_value.hide = track_hide
            mock_window.return_value.show = track_show
            
            app = source_module.piDSLM()
            
            # Test show_busy
            app.show_busy()
            assert len(busy_shown) == 1
            
            # Test hide_busy
            app.hide_busy()
            assert len(busy_hidden) == 1


def test_video_capture(source_module):
    """Test video capture functionality"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            with patch('os.system') as mock_system:
                app.video_capture()
                # Verify raspivid command was called
                mock_system.assert_called_once()
                assert 'raspivid' in mock_system.call_args[0][0]
                assert '-t 30000' in mock_system.call_args[0][0]  # 30 seconds


def test_burst_capture(source_module):
    """Test burst capture functionality"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            with patch('os.system') as mock_system:
                app.burst()
                # Verify raspistill command was called for burst
                mock_system.assert_called_once()
                assert 'raspistill' in mock_system.call_args[0][0]
                assert '-tl 0' in mock_system.call_args[0][0]  # Timelapse 0ms
                assert '-bm' in mock_system.call_args[0][0]  # Burst mode


def test_lapse_capture(source_module):
    """Test timelapse capture functionality"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            with patch('os.system') as mock_system:
                app.lapse()
                # Verify raspistill command was called for timelapse
                mock_system.assert_called_once()
                assert 'raspistill' in mock_system.call_args[0][0]
                assert '-t 3600000' in mock_system.call_args[0][0]  # 1 hour
                assert '-tl 60000' in mock_system.call_args[0][0]  # 60 second intervals


def test_split_hd_30m(source_module):
    """Test split HD 30 minute capture functionality"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            with patch('os.system') as mock_system:
                app.split_hd_30m()
                # Verify raspivid command was called
                mock_system.assert_called_once()
                assert 'raspivid' in mock_system.call_args[0][0]
                assert '-t 1800000' in mock_system.call_args[0][0]  # 30 minutes
                assert '-sg 300000' in mock_system.call_args[0][0]  # Split every 5 minutes


def test_long_preview(source_module):
    """Test long preview functionality"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            with patch('os.system') as mock_system:
                app.long_preview()
                # Verify raspistill command was called with 10 second preview
                mock_system.assert_called_once()
                assert 'raspistill' in mock_system.call_args[0][0]
                assert '-t 10000' in mock_system.call_args[0][0]  # 10 seconds


def test_capture_image(source_module):
    """Test single image capture functionality"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            with patch('os.system') as mock_system:
                app.capture_image()
                # Verify raspistill command was called
                mock_system.assert_called_once()
                assert 'raspistill' in mock_system.call_args[0][0]
                assert '-f' in mock_system.call_args[0][0]  # Full preview


def test_upload_function(source_module):
    """Test Dropbox upload functionality"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            with patch('subprocess.Popen') as mock_popen:
                app.upload()
                # Verify subprocess was called with correct arguments
                mock_popen.assert_called_once()
                args = mock_popen.call_args[0][0]
                assert 'python3' in args
                assert 'dropbox_upload.py' in args
                assert '--yes' in args


def test_fullscreen_functions(source_module):
    """Test fullscreen toggle functions"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            # Test fullscreen
            app.fullscreen()
            assert mock_app.return_value.tk.attributes.called
            
            # Test notfullscreen
            app.notfullscreen()
            assert mock_app.return_value.tk.attributes.call_count >= 2


def test_gpio_setup(source_module):
    """Test GPIO pin setup during initialization"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            with patch('RPi.GPIO') as mock_gpio:
                app = source_module.piDSLM()
                
                # Verify GPIO warnings were disabled first
                mock_gpio.setwarnings.assert_called_once_with(False)
                
                # Verify GPIO mode was set
                mock_gpio.setmode.assert_called_once()
                assert mock_gpio.BCM in mock_gpio.setmode.call_args[0]
                
                # Verify GPIO 16 was set up as input with pull-up
                mock_gpio.setup.assert_any_call(16, mock_gpio.IN, pull_up_down=mock_gpio.PUD_UP)
                
                # Verify event detection was added
                mock_gpio.add_event_detect.assert_called_once()
                assert mock_gpio.add_event_detect.call_args[0][0] == 16
                assert mock_gpio.add_event_detect.call_args[0][1] == mock_gpio.FALLING


def test_picture_index_functions(source_module):
    """Test picture navigation functions"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            # Test picture_left with empty list (edge case)
            app.picture_index = 0
            app.saved_pictures = []
            # This will cause IndexError since there are no pictures
            # but we test the logic before the error
            with pytest.raises(IndexError):
                app.picture_left()
            
            # Test picture_right with empty list
            app.picture_index = 0
            app.saved_pictures = []
            with pytest.raises(IndexError):
                app.picture_right()


def test_show_gallery(source_module):
    """Test gallery window functionality"""
    with patch('guizero.App') as mock_app:
        with patch('guizero.Window') as mock_window:
            mock_app.return_value.display = MagicMock()
            mock_app.return_value.tk = MagicMock()
            mock_app.return_value.tk.attributes = MagicMock()
            mock_window.return_value.hide = MagicMock()
            mock_window.return_value.show = MagicMock()
            
            app = source_module.piDSLM()
            
            # Mock glob to return some test images
            with patch('glob.glob') as mock_glob:
                mock_glob.return_value = ['/home/pi/Downloads/test1.jpg', '/home/pi/Downloads/test2.jpg']
                
                with patch('guizero.PushButton') as mock_button:
                    with patch('guizero.Picture') as mock_picture:
                        app.show_gallery()
                        
                        # Verify gallery window was created
                        assert app.gallery is not None
                        mock_glob.assert_called_once()
                        assert '/home/pi/Downloads/*.jpg' in mock_glob.call_args[0][0]
