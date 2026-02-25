"""Basic functionality tests for piDSLM"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime


def test_timestamp_generation(source_module):
    """Test that timestamp generation works correctly"""
    app = source_module.piDSLM()
    timestamp_str = app.timestamp()
    
    # Verify timestamp format: YYYYMMDD_HHMMSS (15 chars without leading zeros)
    assert len(timestamp_str) == 15
    assert timestamp_str[8] == '_'
    
    # Verify it can be parsed back to datetime
    parsed = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
    assert parsed is not None


def test_clear_folder(source_module):
    """Test clear folder functionality"""
    with patch('pidslm.os.system') as mock_system:
        app = source_module.piDSLM()
        app.clear()
        
        # Verify the rm command was called
        mock_system.assert_called_once_with("rm -v /home/pi/Downloads/*")


def test_show_busy_window(source_module):
    """Test showing busy window"""
    with patch('pidslm.Window') as MockWindow:
        app = source_module.piDSLM()
        
        # Mock the busy window
        app.busy = MagicMock()
        app.show_busy()
        
        # Verify busy window was shown
        app.busy.show.assert_called_once()


def test_hide_busy_window(source_module):
    """Test hiding busy window"""
    with patch('pidslm.Window') as MockWindow:
        app = source_module.piDSLM()
        
        # Mock the busy window
        app.busy = MagicMock()
        app.hide_busy()
        
        # Verify busy window was hidden
        app.busy.hide.assert_called_once()


def test_capture_image(source_module):
    """Test single image capture"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            app.capture_image()
            
            # Verify raspistill command for single image
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspistill' in cmd
            assert '-f' in cmd
            assert 'cam.jpg' in cmd


def test_gpio_setup(source_module):
    """Test GPIO pin setup for button"""
    with patch('pidslm.GPIO') as mock_gpio:
        app = source_module.piDSLM()
        
        # Verify GPIO setup was called
        mock_gpio.setwarnings.assert_called_once_with(False)
        mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
        mock_gpio.setup.assert_any_call(16, mock_gpio.IN, pull_up_down=mock_gpio.PUD_UP)
        mock_gpio.add_event_detect.assert_called_once()


def test_app_initialization(source_module):
    """Test piDSLM app initialization"""
    with patch('pidslm.App') as MockApp:
        with patch('pidslm.Window') as MockWindow:
            with patch('pidslm.PushButton') as MockButton:
                with patch('pidslm.Text') as MockText:
                    with patch('pidslm.Picture') as MockPicture:
                        with patch('pidslm.GPIO') as mock_gpio:
                            app = source_module.piDSLM()
                            
                            # Verify app was created with correct parameters
                            MockApp.assert_called()
                            MockWindow.assert_called()
                            
                            # Verify buttons were created
                            assert MockButton.call_count >= 8


def test_button_event_callback(source_module):
    """Test GPIO button event callback"""
    with patch('pidslm.os.system') as mock_system:
        with patch('pidslm.datetime') as mock_datetime:
            mock_datetime.datetime.now.return_value = datetime(2024, 1, 15, 10, 30, 45)
            
            app = source_module.piDSLM()
            
            # Simulate button press callback
            app.takePicture(16)
            
            # Verify raspistill was called
            mock_system.assert_called_once()
            cmd = mock_system.call_args[0][0]
            assert 'raspistill' in cmd
            assert '-t 3500' in cmd


def test_fullscreen_functions(source_module):
    """Test fullscreen toggle functions"""
    with patch('pidslm.App') as MockApp:
        app = source_module.piDSLM()
        
        # Mock app.tk
        app.app = MagicMock()
        app.app.tk = MagicMock()
        
        # Test fullscreen
        app.fullscreen()
        app.app.tk.attributes.assert_called_with("-fullscreen", True)
        
        # Test notfullscreen
        app.notfullscreen()
        app.app.tk.attributes.assert_called_with("-fullscreen", False)


def test_clear_button_function(source_module):
    """Test clear button functionality"""
    with patch('pidslm.os.system') as mock_system:
        app = source_module.piDSLM()
        app.clear()
        
        # Verify the clear command was called
        mock_system.assert_called_once_with("rm -v /home/pi/Downloads/*")


def test_upload_to_dropbox(source_module):
    """Test Dropbox upload functionality"""
    with patch('pidslm.subprocess.Popen') as mock_popen:
        app = source_module.piDSLM()
        app.upload()
        
        # Verify subprocess was called with correct arguments
        mock_popen.assert_called_once_with(["python3", "/home/pi/piDSLM/dropbox_upload.py", "--yes"])
