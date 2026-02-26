"""Tests for piDSLM - Raspberry Pi DSLR Camera Controller"""
import pytest
import os
import sys
from unittest.mock import MagicMock, patch


def test_app_initialization(source_module):
    """Test that the piDSLM app initializes correctly."""
    with patch('RPi.GPIO') as mock_gpio:
        with patch('guizero.App') as mock_app:
            with patch('guizero.Window') as mock_window:
                # Setup GPIO mock
                mock_gpio.BCM = 11
                mock_gpio.BOARD = 10
                mock_gpio.OUT = 0
                mock_gpio.IN = 1
                mock_gpio.HIGH = 1
                mock_gpio.LOW = 0
                mock_gpio.PUD_UP = 2
                
                # Mock the display method to prevent blocking
                mock_app_instance = MagicMock()
                mock_app_instance.display = MagicMock()
                mock_app_instance.tk = MagicMock()
                mock_app_instance.tk.attributes = MagicMock()
                mock_app.return_value = mock_app_instance
                
                # Initialize the app
                app = source_module.piDSLM()
                
                # Verify app was created
                assert app is not None
                assert hasattr(app, 'app')
                assert hasattr(app, 'busy')


def test_clear_folder(source_module):
    """Test clear folder functionality."""
    with patch('RPi.GPIO') as mock_gpio:
        with patch('os.system') as mock_system:
            mock_system.return_value = 0
            
            app = source_module.piDSLM()
            
            # Test clear
            app.clear()
            
            # Verify os.system was called for clearing folder
            assert mock_system.called
            assert "rm -v" in str(mock_system.call_args)


def test_show_hide_busy(source_module):
    """Test busy indicator functionality."""
    with patch('RPi.GPIO') as mock_gpio:
        app = source_module.piDSLM()
        
        # Test show and hide busy
        app.show_busy()
        app.hide_busy()
        
        # Verify busy indicator methods were called
        assert hasattr(app, 'busy')


def test_burst_mode(source_module):
    """Test burst capture mode."""
    with patch('RPi.GPIO') as mock_gpio:
        with patch('os.system') as mock_system:
            mock_system.return_value = 0
            
            app = source_module.piDSLM()
            
            # Test burst mode
            app.burst()
            
            # Verify raspistill command was called
            assert mock_system.called
            assert "raspistill" in str(mock_system.call_args)


def test_split_hd_30m(source_module):
    """Test 30 minute split recording."""
    with patch('RPi.GPIO') as mock_gpio:
        with patch('os.system') as mock_system:
            mock_system.return_value = 0
            
            app = source_module.piDSLM()
            
            # Test split recording
            app.split_hd_30m()
            
            # Verify raspivid command was called
            assert mock_system.called
            assert "raspivid" in str(mock_system.call_args)


def test_lapse_mode(source_module):
    """Test timelapse mode."""
    with patch('RPi.GPIO') as mock_gpio:
        with patch('os.system') as mock_system:
            mock_system.return_value = 0
            
            app = source_module.piDSLM()
            
            # Test lapse mode
            app.lapse()
            
            # Verify raspistill command was called with timelapse interval
            assert mock_system.called
            call_args = str(mock_system.call_args)
            assert "raspistill" in call_args
            assert "-tl" in call_args  # timelapse interval flag


def test_long_preview(source_module):
    """Test long preview functionality."""
    with patch('RPi.GPIO') as mock_gpio:
        with patch('os.system') as mock_system:
            mock_system.return_value = 0
            
            app = source_module.piDSLM()
            
            # Test long preview
            app.long_preview()
            
            # Verify raspistill command was called
            assert mock_system.called
            assert "15000" in str(mock_system.call_args)


def test_capture_image(source_module):
    """Test single image capture."""
    with patch('RPi.GPIO') as mock_gpio:
        with patch('os.system') as mock_system:
            mock_system.return_value = 0
            
            app = source_module.piDSLM()
            
            # Test capture image
            app.capture_image()
            
            # Verify raspistill command was called
            assert mock_system.called
            assert "raspistill" in str(mock_system.call_args)


def test_video_capture(source_module):
    """Test video capture functionality."""
    with patch('RPi.GPIO') as mock_gpio:
        with patch('os.system') as mock_system:
            mock_system.return_value = 0
            
            app = source_module.piDSLM()
            
            # Test video capture
            app.video_capture()
            
            # Verify raspivid command was called
            assert mock_system.called
            assert "raspivid" in str(mock_system.call_args)


def test_upload_to_dropbox(source_module):
    """Test Dropbox upload functionality."""
    with patch('RPi.GPIO') as mock_gpio:
        with patch('subprocess.Popen') as mock_popen:
            mock_popen.return_value = MagicMock()
            
            app = source_module.piDSLM()
            
            # Test upload
            app.upload()
            
            # Verify subprocess was called for upload
            assert mock_popen.called


def test_timestamp(source_module):
    """Test timestamp generation."""
    with patch('RPi.GPIO') as mock_gpio:
        app = source_module.piDSLM()
        
        # Test timestamp
        ts = app.timestamp()
        
        # Verify timestamp format
        assert isinstance(ts, str)
        assert "_" in ts  # Should have date_time separator


def test_take_picture_callback(source_module):
    """Test picture taking callback."""
    with patch('RPi.GPIO') as mock_gpio:
        with patch('os.system') as mock_system:
            mock_system.return_value = 0
            
            app = source_module.piDSLM()
            
            # Test takePicture callback
            app.takePicture(16)  # Pass channel argument
            
            # Verify raspistill command was called
            assert mock_system.called
            assert "3500" in str(mock_system.call_args)
